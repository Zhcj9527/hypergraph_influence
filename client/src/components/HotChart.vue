<template>
    <div class='hot-chart' ref='root'>
    </div>
</template>

<script>
import * as d3 from 'd3'

export default{
    name:'component_name',
    data(){
        return{

        }

    },
    props:[],
    methods:{
        draw(hotmap_data){
            var data = hotmap_data["data"][0]["value"],
             columns = hotmap_data["columns"]
            // SVG画布边缘与图表内容的距离
            var margin = {top: 10, right: 10, bottom: 30, left: 40},
                width = 550 - margin.left - margin.right,
                height = 700 - margin.top - margin.bottom
            var svg = d3.select('.hot-chart').append('svg')
                .attr('width', width + margin.right + margin.left)
                .attr('height', height + margin.top + margin.bottom)
                .append('g')
                .attr('transform','translate(' + margin.left + ',' + margin.top + ')')

            var y = d3.scaleBand()
                .rangeRound([0, (height + margin.top + margin.bottom)/1.01])
                .padding(0.1)  // 控制每个矩形的间隔
                .align(0.1);

            var x = d3.scaleLinear()
                .rangeRound([(width + margin.right + margin.left)/10, 0]); // 控制宽度

            var z = d3.scaleOrdinal()
                // .range(['#CCCE70', "#98D1C8", "#EDCC63", "#F6F5B3", "#F4D3C1",'#FB5652','#FFB005']);
                // .range(['#2960DE', "#F5E53A", "#96B2FB", "#FFD3D4", "#DB5629",'#FB5652','#FFB005']);
                // .range(['#344D77', "#C55A82", "#FFD34B", "#FF7241", "#62DCDA",'#FB5652','#FFB005']);
                // .range(['#4DB8EF', "#2D5A76", "#FF7B53", "#F7F4EB", "#F7D15C",'#FB5652','#FFB005']);
                // .range(['#264D59', "#43978D", "#F9E07F", "#F9AD6A", "#D46C4E",'#FB5652','#FFB005']);
                // .range(['#ebb0a4', "#84d9d4", "#d8b3e1", "#c4d4a3", "#93c1ed",'#FB5652','#FFB005']); // root
                // .range(['rgb(68, 140, 189)', "rgb(247, 147, 56)", "rgb(78, 173, 80)", "rgb(219, 122,111)", "rgb(161, 127, 196)",'#FB5652','#FFB005']); //DGS
                // .range(['rgb(255, 208, 120)', "rgb(178, 224, 116)", "rgb(189, 217, 246)", "rgb(142, 155, 224)", "rgb(214, 76, 77)",'#FB5652','#FFB005']); //bus
                .range(['rgb(27, 132, 199)', "rgb(63, 214, 214)", "rgb(255, 207, 80)", "rgb(255, 128,101)", "rgb(223, 159, 235)",'#FB5652','#FFB005']); //muluba
                // .range(['#77d1e5', "#ebb0a4", "#9adabe", "#c6b6e5", "#ced39f",'#FB5652','#FFB005']);
                // .range(['#df9feb',"#ff8065","#ffcf50","#3fd6d6", '#1b84c7', "#ced39f",'#FB5652','#FFB005']);

            var stack = d3.stack()
                .offset(d3.stackOffsetExpand)
                .order(d3.stackOrderNone); // 调节顺序

            y.domain(data.map(function(d) {
                  return d.period;
                }));
            // console.log("y",data.map(function(d) {
            //       return d.period;
            //     }))

            z.domain(columns.slice(1));
            console.log("z", columns.slice(1))

            // 添加的是y轴
            svg.append("g")
                    .attr("class", "axis axis--y")
                    .call(d3.axisLeft(y));

            // // 分类别颜色图例
            // var legend = svg
            //     .append('g')
            //     .attr("class", "legend")
            //     .selectAll("g")
            //     .data(columns.slice(1))
            //     .enter().append("g")
            //     .attr("id", d => 'legend_group-'+ d )
            //     .attr("transform", function (d, i) {
            //         return "translate(300," + (i * 20) + ")";
            //     });
            //
            // legend.append("rect")
            //     .attr("width", 18)
            //     .attr("height", 18)
            //     .style("fill", z);
            //
            // legend.append("text")
            //     .attr("x", 24)
            //     .attr("y", 9)
            //     .attr("dy", ".35em")
            //     .text(function (d) {
            //         return d;
            //     });

            svg.append('g')
                // .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
                .attr("class", "algorithm")
                .selectAll("g")
                .data(hotmap_data["data"])
                .enter().append("g")
                .attr("id", d => 'algorithm_group-'+ d.id)
                .attr("transform", function (d, i) {
                    return "translate(" + (i * 61)  + ",0)";
                })
                // .on("click",  (d) => {
                //     this.$bus.$emit('algorithm-selected-hot',
                //         {"algorithm": d.id})
                // })
                // .on("dblclick", (d) => {
                //     this.$bus.$emit('algorithm-selected-hot-dbl',
                //         {"algorithm": d.id})
                // })
                .on("click", (d) => _click(d))
                .on("dblclick", (d) => _doublelclick(d))
                .on("mouseover", d => {
                    this.$bus.$emit("alg-mouseover", d.id) // 鼠标悬浮在指定的node上，在left-text显示
                })
                .each(multiple)
                .select("g");

            function multiple(d) {

                var svg = d3.select(this)
                    .append("g")

                var serie = svg.selectAll(".serie")
                    .data(stack.keys(columns.slice(1))(d.value))
                    .enter().append("g")
                    .attr("class", "serie")
                    .attr("fill", function (d) {
                        return z(d.key);
                    });
                // console.log("serie_data", stack.keys(columns.slice(1))(data))

                serie.selectAll("rect")
                    .data(function (d) {
                        return d;
                    })
                    .enter().append("rect")
                    .attr("y", function (d) {
                        return y(d.data.period);
                    })
                    .attr("x", function (d) {
                        return x(d[1]);
                    })
                    .attr("width", function (d) {
                        return x(d[0]) - x(d[1]);
                    })
                    // .attr("transform", "translate(0," + 2 + ")")
                    .attr("height", y.bandwidth());

            }

            //测试单击事件(如果一个元素中同时有单击事件和双击事件的话，会存在冲突)
            var clickTimer = null,
                vm = this;

            function _click(d) {
                if (clickTimer) {
                    window.clearTimeout(clickTimer);
                    clickTimer = null;
                }
                clickTimer = window.setTimeout(function() {
                    // your click process code here
                    vm.$bus.$emit('algorithm-selected-hot',
                        {"algorithm": d.id})
                    // alert("你单击了我");
                }, 300);

            }

            function _doublelclick(d) {
                if (clickTimer) {
                    window.clearTimeout(clickTimer);
                    clickTimer = null;
                }
                // your click process code here
                vm.$bus.$emit('algorithm-selected-hot-dbl',
                        {"algorithm": d.id})
                // alert("你双击了我");
            }

            // var legend = serie.append("g")
            //     .attr("class", "legend")
            //     .attr("transform", function(d) {
            //         var d = d[0];
            //         return "translate(" +  ((x(d[0]) + x(d[1])) / 2) + ", " +(y(d.data.period) - y.bandwidth())+ ")";
            //     });
            //
            // legend.append("line")
            //     .attr("y1", 5)
            //     .attr("x1", 15)
            //     .attr("x2", 15)
            //     .attr("y2", 12)
            //     .attr("stroke", "#000");
            //
            // legend.append("text")
            //     .attr("x", 9)
            //     .attr("dy", "0.35em")
            //     .attr("fill", "#000")
            //     .style("font", "10px sans-serif")
            //     .text(function(d) {
            //         return d.key;
            //     });

        }

    },
    computed:{

    },
    watch:{

    },
    created(){

    },
    mounted(){
        this.$axios.get('get_hotmap_data')
            .then((res) =>{
                var hotmap_data = res.data
                console.log(hotmap_data) // object
                this.draw(hotmap_data)
            })
            .catch((error) =>{
                console.log('get_hotmap_data', error)
            })

        // // 默认值是Restaurant-Rev，可以先不要，点击dataset后就可以生成hotmap
        // this.$axios.post('get_hotmap_data', "Restaurants-Rev")
        //     .then((res) => {
        //         d3.select('.hot-chart').selectAll('*').remove();  // 移除原来的画布所画内容
        //         var hotmap_data = res.data
        //         console.log("algorithm_data", hotmap_data);
        //         this.draw(hotmap_data)
        //     })
        //     .catch((error) => {
        //         console.log('get_hotmap_data', error);
        //     })


        // // 事件触发后->改变算法
        // this.$bus.$on('dataset-selected-control panel', (d) => {
        //     console.log(d)
        //     this.$axios.post('get_hotmap_data', d.dataset)
        //     .then((res) => {
        //         d3.select('.hot-chart').selectAll('*').remove();  // 移除原来的画布所画内容
        //         var hotmap_data = res.data
        //         console.log("algorithm_data", hotmap_data);
        //         this.draw(hotmap_data)
        //     })
        //     .catch((error) => {
        //         console.log('get_hotmap_data', error);
        //     })
        // })

        // this.$axios.post('get_selected_steps',{
        //     stepSelected: 2,
        //     flag: true
        //     })
        //     .then((res) => {
        //         var data = res.data
        //         console.log(data)
        //     })
        //     .catch((error) => {
        //         console.log('get_selected_steps', error)
        //     })

    }
}
</script>

<style>
  .bar {
      fill: steelblue;
  }

  .axis path {
      display: none;
  }
</style>