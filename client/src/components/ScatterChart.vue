<template>
    <div class='scatter-chart' ref='root'>
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
        draw(data){
            var margin = {top: 10, right: 20, bottom: 10, left: 21},
                width = 520 - margin.left - margin.right,
                height = 320 - margin.top - margin.bottom;

            var padding = 20;

            var c_r=8;

            // var cluster_color = ['#ebb0a4', "#84d9d4", "#d8b3e1", "#c4d4a3", "#93c1ed",'#FB5652','#FFB005']; //ori
            // var cluster_color = ['rgb(255, 208, 120)', "rgb(178, 224, 116)", "rgb(189, 217, 246)", "rgb(142, 155, 224)", "rgb(214, 76, 77)",'#FB5652','#FFB005']; //bus
            var cluster_color = ['rgb(68, 140, 189)', "rgb(247, 147, 56)", "rgb(78, 173, 80)", "rgb(219, 122,111)", "rgb(161, 127, 196)",'#FB5652','#FFB005']; //DGS

            var svg = d3.select('.scatter-chart').append('svg')
                .attr('width', width + margin.left + margin.right).attr('height', height + margin.top + margin.bottom)
                .append('g')
                .attr('transform','translate(' + margin.left + ',' + margin.bottom + ')');

            // x轴
            var xScale = d3.scaleLinear()
                .domain([d3.min(data, function(d) { return parseInt(d.x); })-0.9, d3.max(data, function(d) { return parseInt(d.x)+0.9;})])
                // .domain([-11.5, d3.max(data, function(d) { return parseInt(d.x)+0.9;})])
                .range([ 0, width]);
            svg.append('g')
                .attr("class", "x-axis")
                .attr('transform','translate(0, ' + (height) + ')')
                .call(d3.axisBottom(xScale));

            var z = d3.scaleOrdinal()
                // .range(['#CCCE70', "#98D1C8", "#EDCC63", "#F6F5B3", "#F4D3C1",'#FB5652','#FFB005'])
                .range(cluster_color);

            z.domain(["4", "3", "2", "1", "0"]);

            // y轴
            var yScale = d3.scaleLinear()
                .domain([d3.min(data, function(d) { return parseInt(d.y)-0.9; }), d3.max(data, function(d) { return parseInt(d.y)+0.9; })])
                // .domain([-8, d3.max(data, function(d) { return parseInt(d.y)+0.9; })])
                .range([ height, padding ]);
            svg.append('g')
                .attr("class", "y-axis")
                .call(d3.axisLeft(yScale));

            // //原点坐标
            // var rScale = d3.scaleLinear()
            //     .domain([0, d3.max(data, function(d) {
            //         return d.y;
            //     })])
            //     .range([2, 20]);

            // 散点图，点（circle）
            svg.append("g")
                .attr("class", "circle")
                .selectAll("circle")
                .data(data)
                .enter()
                .append("circle")
                .attr("id", d => "vg-" +d.name)
                .attr("cx", function(d) {
                    return xScale(d.x);
                })
                .attr("cy", function(d) {
                    return yScale(d.y);
                })
                // .attr("r", function(d) {
                //     return rScale(d.y);
                // })
                .attr("r", c_r)
                // .attr("fill","teal");
                .attr("fill", d => {
                    return z(d.id);
                })

            //标签
            svg.append("g")
                .attr("class", "myText")
                .selectAll("myText")
                .data(data)
                .enter()
                .append("text")
                .attr("id", d => "text-" +d.name)
                .text(function(d) {
                    return d.id + "  " + d.name;
                })
                .attr("x", function(d) {
                     return xScale(d.x)
                })
                .attr("y", function(d) {
                    return yScale(d.y);
                })
                .attr("dx", function() {
                    return 5
                })
                .attr("dy", function() {
                    return -5
                })
                .attr("font-family", "sans-serif")
                .attr("font-size", "11px")
                .attr("fill", "steelblue");

            d3.select(".myText").style("visibility", "hidden")
            d3.select(".x-axis").style("visibility", "hidden")
            d3.select(".y-axis").style("visibility", "hidden")

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
            this.$axios.post('get_scatter_data', d.algorithm)
            .then((res) => {
                d3.select('.scatter-chart').selectAll('*').remove();  // 移除原来的画布所画内容
                var data = res.data
                console.log("scatter_data", data);

                var seeds = [] // 获取最终的激活节点，传到Structure View
                data.forEach( d => {
                    seeds.push(d.name)
                } )
                this.$bus.$emit("final-nodes", seeds)

                this.draw(data)

            })
            .catch((error) => {
                console.log('get_scatter-chart', error);
            })
        })

        var periodList = []
        this.$bus.$on("selected_period_included_vg", period_vg => {
            d3.selectAll(".circle").attr("visibility", "hidden")

            if (periodList !== period_vg) {
                period_vg.forEach( d => {
                    d3.select("#vg-" + d.node).style("visibility", "visible")
                    d3.select("#text-" + d.node).style("visibility", "visible")
                })
                console.log(period_vg)
                periodList.forEach( d => {
                    d3.select("#vg-" + d.node).style("visibility", "hidden")
                    d3.select("#text-" + d.node).style("visibility", "hidden")
                })
                console.log(periodList)
            }
            periodList = period_vg
        })

        this.$bus.$on("highlighted_vg-mouseover", d => {
            d3.select("#vg-" + d)
                .attr("r", 15)
                // .style("stroke-dasharray", "blue")
                // .style("stroke-width", 5)
        })
        this.$bus.$on("highlighted_vg-mouseout", d => {
            d3.select("#vg-" + d)
                .attr("r", 5)
                // .style("stroke", "steelblue")
                // .style("stroke-width", 2)
        })

        // this.$axios.get('get_scatter_data')
        // .then((res) =>{
        //     var data = res.data
        //     console.log(data)
        //     this.draw(data)
        // })
        // .catch((error) =>{
        //     console.log('get_scatter_data', error)
        // })

    }
}
</script>
