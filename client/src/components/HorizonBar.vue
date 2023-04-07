<template>
    <div class='horizon-bar' ref='root'>
    </div>
</template>

<script>
import * as d3 from '../assets/js/d3/d3.v3.js'

export default{
    name:'component_name',
    data(){
        return{

        }

    },
    props:[],
    methods:{
        draw_HB(data){
            var data_left = data[0]["value"],
                data_right = data[1]["value"];

            // SVG画布边缘与图表内容的距离
            var margin = {top: 10, right: 30, bottom: 10, left: 30},
                width = 158 - margin.left - margin.right,
                height = 460 - margin.top - margin.bottom
                // height = 654 - margin.top - margin.bottom
            var svg = d3.select('.horizon-bar').append('svg')
                .attr('width', width + margin.left + margin.right)
                .attr('height', height + margin.top + margin.bottom)
                .append('g')
                // .attr('transform','translate(' + margin.left + ',' + margin.top + ')');

            var barHeight = 15,
                rectOffset = 34,
                svgOffset = 23;  // 整个horizontal-svg向下移动的距离

            var x1 = d3.scale.linear()
                .range([0, width/2])
                .domain([0, d3.max(data_left, function(d) { return parseInt(d.sup); })]);

            var x2 = d3.scale.linear()
                .range([0, width/2])
                .domain([0, d3.max(data_right, function(d) { return parseInt(d.sup); })]);

            var left_g = svg.append("g")
                .attr("class", "left bar")
                .attr("width", width/2)
                .attr("height", height)
                .attr("transform",  "translate(0," + svgOffset + ")") // 向下偏移

            var left_bar = left_g.selectAll("g")
                .data(data_left)
                .enter().append("g")
                .attr("transform", function(d, i) { return "translate(0," + i * rectOffset + ")"; });

            left_bar.append("rect")
                .attr("width", function(d) { return x1(parseInt(d.sup)); })
                .attr("height", barHeight - 1)
                // .style("fill", "rgb(112, 128, 144)")
                .style("fill", d => "rgb(112,128,144," + (d.coverage*1.5) + ")")
                .attr("transform",  function(d) { return "translate(" + ((width + margin.left + margin.right)/2 - x1(parseInt(d.sup))) + ",0)" ;})
                .on("mouseover", d => {
                    this.$bus.$emit("left-rect-mouseover", parseInt(d.sup)) // 鼠标悬浮在指定的node上，在left-text显示
                })
                .on("mouseout", d => {
                    this.$bus.$emit("left-mouseout", parseInt(d.sup)) // 鼠标移除指定的node上，在parallel视图恢复显示
                });

            // left_bar.append("text")
            //     .attr("x", function(d) { return x(d.value) - 3; })
            //     .attr("y", barHeight / 2)
            //     .attr("dy", ".35em")
            //     .text(function(d) { return d.value; });

            var right_g = svg.append("g")
                .attr("class", "right bar")
                .attr("width", width/2)
                .attr("height", height)
                .attr("transform",  "translate(0," + svgOffset + ")") // 向下偏移

            var right_bar = right_g.selectAll("g")
                .data(data_right)
                .enter().append("g")
                .attr("transform", function(d, i) { return "translate("+ (width + margin.left + margin.right)/2 + "," + i * rectOffset + ")"; });

            right_bar.append("rect")
                .attr("width", function(d) { return x2(parseInt(d.sup)); })
                .attr("height", barHeight - 1)
                // .style("fill", "#69b3a2")
                .style("fill", d => "rgb(112,128,144," + (d.coverage*1.5) + ")")
                // .attr("transform",  function(d) { return "translate(0," + x2(d.value)+ ")" ;})
                .on("mouseover", d => {
                    this.$bus.$emit("right-rect-mouseover", parseInt(d.sup)) // 鼠标悬浮在指定的node上，在left-text显示
                })
                .on("mouseout", d => {
                    this.$bus.$emit("right-mouseout", parseInt(d.sup)) // 鼠标移除指定的node上，在parallel视图恢复显示
                });

            svg.append("line")
                .attr("class", "mid line")
                .attr("x1", (width + margin.left + margin.right)/2)
                .attr("y1", 0)
                .attr('x2', (width + margin.left + margin.right)/2)
                .attr("y2", height + margin.top + margin.bottom)
                .style("stroke", "#e5e5e7")
                .style("stroke-width", "2")





        }

    },
    computed:{

    },
    watch:{

    },
    created(){

    },
    mounted(){
        // this.$axios.get('get_HorizonBar_data')
        //     .then((res) =>{
        //         var data = res.data
        //         console.log(data)
        //         this.draw_HB(data)
        //     })
        //     .catch((error) =>{
        //         console.log('getHorizonBar_data', error)
        //     })

        var default_horizonBar = []
        this.$bus.$on('default_Alg_A', (d) => {
            default_horizonBar.push(d[0])
            this.$bus.$on('default_Alg_B', (d) => {
                default_horizonBar.push(d[0])
                console.log("default_horizonBar",  default_horizonBar)
                this.draw_HB(default_horizonBar)
            })
        })

        var click_horizonBar = []
        this.$bus.$on('click_Alg_A', (d) => {
            d3.select('.horizon-bar').selectAll('*').remove();  // 移除原来的画布所画内容
            click_horizonBar.push(d[0])
            this.$bus.$on('dblclick_Alg_B', (d) => {
                click_horizonBar.push(d[0])
                console.log("click_horizonBar", click_horizonBar)
                this.draw_HB(click_horizonBar)
            })
        })

        var selected_horizonBar = [] //先A后B
        this.$bus.$on('selected-pat1_Alg_A', (d) => {
            d3.select('.horizon-bar').selectAll('*').remove();  // 移除原来的画布所画内容
            selected_horizonBar.push(d[0])
            this.$bus.$on('selected-pat2_Alg_B', (d) => {
                selected_horizonBar.push(d[0])
                console.log("selected_horizonBar", selected_horizonBar)
                this.draw_HB(selected_horizonBar)
            })
        })

        var selected_horizonBar1 = [] //先B后A
        this.$bus.$on('selected-pat2_Alg_B', (d) => {
            d3.select('.horizon-bar').selectAll('*').remove();  // 移除原来的画布所画内容
            selected_horizonBar1.push(d[0])
            this.$bus.$on('selected-pat1_Alg_A', (d) => {
                selected_horizonBar1.push(d[0])
                console.log("selected_horizonBar1", selected_horizonBar1)
                this.draw_HB(selected_horizonBar1)
            })
        })




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