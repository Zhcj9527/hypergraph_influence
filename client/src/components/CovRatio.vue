<template>
    <div class='cov-ratio' ref='root'>
    </div>
</template>

<script>
import * as d3 from 'd3'
import "../assets/js/d3/d3.tip.js"


export default{
    name:'CovRatio',
    data(){
        return{

        }

    },
    props:[],
    methods:{
        drawBar(barData, barData_ind, nodesData){
            // SVG画布边缘与图表内容的距离
            var margin = {top: 10, right: 20, bottom: 20, left: 10},
                width = 796 - margin.left - margin.right,
                height_svg = 330 - margin.top - margin.bottom
            var svg = d3.select('.cov-ratio').append('svg')
                .attr('width', width + margin.left + margin.right)
                .attr('height', height_svg + margin.top + margin.bottom )
                // .attr('width', width)
                // .attr('height', height_svg )

            // var svg2 = svg.append('g')
            //     .attr('width', width + margin.left + margin.right)
            //     .attr('height', 300)

            var bar_top_height = 30,
                bar_bottom_height = 20,
                circle_height = 250,
                // origin
                // bar_top_color = "#ff4a84",
                // bar_bottom_color = "rgb(244,177,131)"
                bar_top_color = "rgb(213,132,189)",
                bar_bottom_color = "rgb(193,196,72)"

            var g_bar_top = svg
                .append('g')
                .attr('height', bar_top_height)
                .attr("class", "g_bar_top")
                .attr('transform','translate(' + margin.left + ',' + margin.top + ')')

            // // tip
            // var tip = d3.tip()
            //     .attr('class', 'd3-tip')
            //     .offset([-10, 0])
            //     .html(function(d) {
            //         return d.id + ": <span style='color:orangered'>" + d.value + "</span>";
            //     });
            //
            // svg.call(tip);
            console.log(barData)
            barData.forEach( d => {
                if (d.id === "P24") {
                    this.$bus.$emit("selected_cum-mouseover", d.value)
                }
            })

            // X axis
            var x = d3.scaleBand()
                .domain(barData.map(function (d) {
                    return d.id;
                }))
                .range([0, width])
                .padding(0.2)

            var rect = g_bar_top.append('g')
                .attr("class", "axis-bar")
                .attr('transform', 'translate(0,' + height_svg + ')')
                .style("font-size", 8)
                .call(d3.axisBottom(x).tickSize(5))

            // Add Y axis
            var y = d3.scaleLinear()
                .domain([0, d3.max(barData, function (d) {
                    return d.value
                })])
                .range([bar_top_height, 0])


            // g_bar.append('g')
            //     .call(d3.axisLeft(y))
            //     .style("visibility", "hidden");

            // Bars
            g_bar_top.selectAll('rect')
                .data(barData)
                .enter()
                .append('rect')//利用enter 创建与数据个数一样的rect矩形
                .attr("id", function (d) {
                    return d.id;
                })
                .attr("x", function (d) {
                    return x(d.id);
                })
                .attr("y", function (d) {
                    return y(d.value);
                })
                .attr("width", x.bandwidth())
                .attr("height", function (d) {
                    return bar_top_height - y(d.value);
                })
                // .attr("fill", "#69b3a2")
                .attr("fill", bar_top_color)
                // .on('mouseover', tip.show)
                // .on('mouseout', tip.hide);
                // .on("mouseover", d => {
                //     this.$bus.$emit("selected_cum-mouseover", d.value) // 鼠标悬浮在指定的node上，在parallel视图上高亮显示
                // })


            var g_bar_bottom = svg
                .append('g')
                .attr('height', bar_bottom_height)
                .attr("class", "g_bar_bottom")
                .attr('transform','translate(' + margin.left + ',' + (margin.top+bar_top_height+5) + ')') // 间距

            // Add Y axis
            var y1 = d3.scaleLinear()
                .domain([0, d3.max(barData_ind, function (d) {
                    return d.value
                })])
                .range([bar_bottom_height, 0])

            // Bars
            g_bar_bottom.selectAll('rect')
                .data(barData_ind)
                .enter()
                .append('rect')//利用enter 创建与数据个数一样的rect矩形
                .attr("id", function (d) {
                    return d.id;
                })
                .attr("x", function (d) {
                    return x(d.id);
                })
                .attr("y", function (d) {
                    return y1(d.value);
                })
                .attr("width", x.bandwidth())
                .attr("height", function (d) {
                    return bar_bottom_height - y1(d.value);
                })
                .attr("transform",  function (d) {
                    return `translate(0, -${y1(d.value)})`
                })
                // .attr("fill", "#69b3a2")
                .attr("fill", bar_bottom_color)
                .on("mouseover", d => {
                    this.$bus.$emit("selected_ind-mouseover", d.value) // 鼠标悬浮在指定的node上，在parallel视图上高亮显示
                })


            var g_circle = svg.append('svg')
                // .attr('width', width + margin.left + margin.right)
                .attr('height', 300)
                // .append('g')
                // .attr('height', circle_height)
                .attr("class", "svg_circle")
                // .attr('transform','translate(' + margin.left + ',' + bar_height + ')')
                // .attr('transform','translate(25,' + 82 + ')')
                // .attr('transform','translate(25,' + 32 + ')') // 圆的画布位置
                .attr('transform','translate(25,' + 32 + ')') // 圆的画布位置 svg2


            // var cluster_color = ['#ebb0a4', "#84d9d4", "#d8b3e1", "#c4d4a3", "#93c1ed",'#FB5652','#FFB005']; //ori
            // var cluster_color = ['rgb(255, 208, 120)', "rgb(178, 224, 116)", "rgb(189, 217, 246)", "rgb(142, 155, 224)", "rgb(214, 76, 77)",'#FB5652','#FFB005']; //bus
            // var cluster_color = ['rgb(68, 140, 189)', "rgb(247, 147, 56)", "rgb(78, 173, 80)", "rgb(219, 122,111)", "rgb(161, 127, 196)",'#FB5652','#FFB005']; //DGS
            // var cluster_color = ['rgb(27, 132, 199)', "rgb(63, 214, 214)", "rgb(255, 207, 80)", "rgb(255, 128,101)", "rgb(223, 159, 235)",'#FB5652','#FFB005']; //muluba
            var cluster_color = ["#9E0041", "#C32F4B", "#E1514B", "#F47245", "#FB9F59", "#FEC574", "#FAE38C", "#EAF195", "#C7E89E", "#9CD6A4", "#6CC4A4",
                                "#4D9DB4", "#4776B4", "#5E4EA1"] // 比较视图

            //  pie_chart data
            this.pie_data = nodesData[0]["values"][2]["values"]
            console.log("pie_data", this.pie_data)
            this.category_num = this.pie_data[0].category_num  // used
            console.log("category_num",this.category_num)
            this.categoryId = this.pie_data[0].category
            console.log("categoryId", this.categoryId)


            //     // 原来可以按照 sum 总和衡量大小的
            // var radius = d3.scaleSqrt()
            //     .domain([0, d3.max(this.pie_data, function (d) {
            //         return parseInt(d.sum);
            //     })])
            //     .range([0, 35]);

                //  自己按照
            var radius = d3.scaleSqrt()
                .domain([0, 226])
                .range([0, 18]);


            // var formatSum = d3.format(".1s");

            // var padding = 10;

            var color = d3.scaleOrdinal()
                .domain(this.category_num)
                // .range(["#f8e765", "#5a8edb", "#61db86","#de57ce" , "#e77652"]);
                // .range(['#CCCE70', "#98D1C8", "#EDCC63", "#F6F5B3", "#F4D3C1",'#FB5652','#FFB005'])
                .range(cluster_color);

            var arc = d3.arc()
                .padRadius(50);

            var pie = d3.pie()
                .sort(null)
                .padAngle(0.05)
                .value(function (d) {
                    return d.values;
                });

            var algorithm_svg = g_circle.append('g')
                .attr('height', circle_height)
                .attr('transform', 'translate(' + 5 + ',' + 0 + ')')
                .attr("class", "algorithm")
                .selectAll("g")
                .data(nodesData)
                .enter().append("g")
                .attr("id", d => 'algorithm_group-'+ d.name)
                .attr("transform", "translate(24,26)");
                // .on("click", )  //添加事件，点击pie 会显示对应的层层之间的比较

            var period_svg = algorithm_svg.append("g")
                .attr("class", "period")
                .selectAll("g")
                .data(d => d.values)
                .enter().append("g")
                .attr("id", d => "period_group-" + d.period)
                .attr("transform", function (d, i) {
                    // return "translate(0," + (i * 20)  + ")";
                    return "translate(" + (i * 30.3)  + ",0)";
                })
                .attr('height', circle_height)
                .on("click", d => {
                    this.$bus.$emit("selected_period_included_vg", d.values)  // 点击指定的period，其所包含的nodes 都突出现实中在parallel视图上
                });

            var pie_svg = period_svg.selectAll(".pie")
                .data(d => d.values)
                .enter().append("g")
                .attr("class", "pie")
                .attr("id", d => 'pie_group-'+ d.node )
                .on("mouseover", d => {
                    this.$bus.$emit("selected_vg-mouseover", d.node) // 鼠标悬浮在指定的node上，在parallel视图上高亮显示
                })
                .on("mouseout", d => {
                    this.$bus.$emit("selected_vg-mouseout", d.node) // 鼠标移除指定的node上，在parallel视图恢复显示
                })
                .each(multiple)
                .select("g");


            var label = pie_svg.append("text")
                .attr("class", "label")
                .attr("font-size", "10px")  // 设置文本大小
                .style("visibility","hidden");

            label.append("tspan")
                .attr("class", "label-name")
                .attr("x", "-1.1em")
                .attr("dy", "-.2em")
                .text( d => d.node );

            label.append("tspan")
                .attr("class", "label-value")
                .attr("x", "-1.1em")
                .attr("dy", "1.1em")
                .text( d => d.sum );

            function multiple(d, i) {
                // var r = radius(parseInt(d.sum));
                var r = radius(75);

                var svg = d3.select(this)
                    .append("g")
                    // .attr("transform", "translate(" +  (2*r*i + 25) + "," + 35 + ")");
                    .attr("transform", "translate(0," + (2*r*i + 50) + ")");

                svg.selectAll(".arc")
                    .data(function (d) {
                        return pie(d.category_list);
                    })
                    .enter().append("path")
                    .attr("class", "arc")
                    .attr("d", arc.outerRadius(r).innerRadius(r * 0.6))
                    .style("fill", function (d) {
                        // console.log(d)
                        // return color(d.data.id);
                        return color(d.data.color);
                    })
                    .attr("stroke", "whitesmoke")
                    .attr("stroke-width", 0.5);
            }


            var brush = d3.brushX()
                .extent([[0, 0], [width, height_svg]])
                .on("start brush", brushed)
                .on("end", brushended);

            // brush
            g_bar_top.append("g")
                .call(brush)
                .call(brush.move, ["P5", "P6"].map(x))
              .selectAll(".overlay")
                .each(function(d) { d.type = "selection"; }) // Treat overlay interaction as move.
                .on("mousedown touchstart", brushcentered); // Recenter before brushing.

            function brushcentered() {
              var dx = x(1) - x(0), // Use a fixed width when recentering.
                  cx = d3.mouse(this)[0],
                  x0 = cx - dx / 2,
                  x1 = cx + dx / 2;
              d3.select(this.parentNode).call(brush.move, x1 > width ? [width - dx, width] : x0 < 0 ? [0, dx] : [x0, x1]);
            }

            function brushed() {
              if (!d3.event.selection) return; // Ignore empty selections.
              var extent = d3.event.selection.map(x.invert, x);
              rect.classed("selected", function(d) { return extent[0] <= d[0] && d[0] <= extent[1]; });
            }

            function brushended() {
              if (!d3.event.sourceEvent) return; // Only transition after input.
              if (!d3.event.selection) return; // Ignore empty selections.
              var d0 = d3.event.selection.map(x.invert),
                  d1 = d0.map(Math.round);

              // If empty when rounded, use floor & offset instead.
              if (d1[0] >= d1[1]) {
                d1[0] = Math.floor(d0[0]);
                d1[1] = d1[0] + 1;
              }

              d3.select(this).transition().call(brush.move, d1.map(x));
            }


        }

    },
    computed:{

    },
    watch:{

    },
    created(){

    },
    mounted(){
        this.$bus.$on('algorithm-selected-hot', (d) => {
            console.log(d)
            this.$axios.post('get_covratio_data', d.algorithm)
            .then((res) => {
                console.log(res)
                console.log(typeof res.data)
                d3.select('.cov-ratio').selectAll('*').remove();  // 移除原来的画布所画内容
                var Cov_data = JSON.stringify(res.data)
                var data = JSON.parse(Cov_data)
                console.log("Cov_data", data); // string
                var barData = data["barData"],
                    barData_ind = data["barData_ind"],
                    nodesData = data["nodesData"]
                this.drawBar(barData, barData_ind, nodesData)

                // this.$bus.$on('radio-selected-cov', (d) => {
                //     if (d.name === "Individual coverage" ) {
                //         d3.select('.cov-ratio').selectAll('*').remove();  // 移除原来的画布所画内容
                //         let barData = data["barData_ind"],
                //             nodesData = data["nodesData"]
                //         this.drawBar(barData, nodesData)
                //     } else {
                //         d3.select('.cov-ratio').selectAll('*').remove();  // 移除原来的画布所画内容
                //         let barData = data["barData"],
                //             nodesData = data["nodesData"]
                //         this.drawBar(barData, nodesData)
                //     }
                // })

            })
            .catch((error) => {
                console.log('get_covratio_data', error);
            })
        })

    }
}
</script>
<style>

    /*.axis-bar .domain {*/
    /*  display: none;*/
    /*}*/

    .d3-tip {
      line-height: 1;
      font-weight: bold;
      padding: 12px;
      background: rgba(0, 0, 0, 0.8);
      color: #fff;
      border-radius: 2px;
    }

    /* Creates a small triangle extender for the tooltip */
    .d3-tip:after {
      box-sizing: border-box;
      display: inline;
      font-size: 10px;
      width: 100%;
      line-height: 1;
      color: rgba(0, 0, 0, 0.8);
      content: "\25BC";
      position: absolute;
      text-align: center;
    }

    /* Style northward tooltips differently */
    .d3-tip.n:after {
      margin: -1px 0 0 0;
      top: 100%;
      left: 0;
    }

    .axis-bar path {
      display: none;
    }


</style>