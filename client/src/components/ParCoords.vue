<template>
    <div class='par-coords' ref='root'>
    </div>
</template>

<script>
import * as d3 from '../assets/js/d3/d3.v3.js'
// import $ from 'jquery'
// import '../assets/js/d3/d3.parcoords.js'
// import '../assets/css/d3.parcoords.css'

export default{
    name:'ParCoords',
    data(){
        return{

        }

    },
    props:[],
    methods:{
        draw(data){
            // SVG画布边缘与图表内容的距离
            var margin = {top: 30, right: 10, bottom: 10, left: 10},
                width = 912 - margin.left - margin.right,
                height = 320 - margin.top - margin.bottom;

            var x = d3.scale.ordinal().rangePoints([0, width], 1),
                y = {};

            var z = d3.scale.ordinal()
                // .range(['#CCCE70', "#98D1C8", "#EDCC63", "#F6F5B3", "#F4D3C1",'#FB5652','#FFB005'])
                .range(['#ebb0a4', "#84d9d4", "#d8b3e1", "#c4d4a3", "#93c1ed",'#FB5652','#FFB005']);

            var line = d3.svg.line(),
                axis = d3.svg.axis(),
                // background,
                foreground;

            var svg = d3.select('.par-coords').append('svg')
                .attr('width', width + margin.left + margin.right)
                .attr('height', height + margin.top + margin.bottom)
                .append('g')
                .attr('transform','translate(' + margin.left + ',' + margin.top + ')')


            // Extract the list of dimensions and create a scale for each.
            var dimensions= ["id", "node_degree", "egonet_neighbor_degree", "egonet_neighbor_edges", "av_degree", "ave_alter_alter_num",
                            "clustering_coefficient", "he_1","he_2","he_3","he_4","he_5" ]

            dimensions.forEach(function(d) {
                return y[d] = d3.scale.linear()
                    .domain(d3.extent(data, function(p) { return +p[d]; }))
                    .range([height, 0]);
            })

            x.domain(dimensions);

            z.domain(["4", "3", "2", "1", "0"]);

            // console.log(dimensions)
            // console.log(y)

            // Add grey background lines for context.
            // background = svg.append("g")
            svg.append("g")
                .attr("class", "background")
                .selectAll("path")
                .data(data)
                .enter().append("path")
                .attr("d", path);

            // Add blue foreground lines for focus.
            foreground = svg.append("g")
                .attr("class", "foreground")
                .selectAll("path")
                .data(data)
                .enter().append("path")
                .attr("id", d => "vg-" +d.name)
                .style("stroke", function (d) {
                        return z(d.id);
                    })
                .attr("d", path)
                // .attr("visibility", d =>{
                //     // d3.selectAll(".foreground").style("visibility", "hidden")
                //
                //     var id = d.name
                //
                //     this.$bus.$on("selected_period_included_vg", period_vg => {
                //         d3.selectAll(".foreground").style("visibility", "hidden")
                //         period_vg.forEach(d => {
                //             if (d.node === id) {
                //                 d3.selectAll("#vg-" + d.node).style("visibility", "visible")
                //             }
                //         })
                //     })

                        // if (c.id === id) return "visible";
                        // else return "hidden"

                // });

            // this.$bus.$on("vgId-selected-par", (d) => {
            //     let vg_name = d.id
            // })

            // Add a group element for each dimension.
            var g = svg.selectAll(".dimension")
                .data(dimensions)
                .enter().append("g")
                .attr("class", d => { return  "dimension-" + d })
                .attr("transform", function(d) { return "translate(" + x(d) + ")"; });

            // Add an axis and title.
            g.append("g")
                .attr("class", "axis-par")
                .each(function(d) { d3.select(this).call(axis.scale(y[d]).orient("left")); })
                .append("text")
                .style("text-anchor", "middle")
                .attr("y", -9)
                .text(function(d) { return d; });

            // choose "id" axis, change style
            d3.select(".dimension-id").call(axis.scale(y["id"]).orient("left").ticks(5));

            // Add and store a brush for each axis.
            g.append("g")
                .attr("class", "brush")
                .each(function(d) { d3.select(this).call(y[d].brush = d3.svg.brush().y(y[d]).on("brush", brush)); })
                .selectAll("rect")
                .attr("x", -8)
                .attr("width", 16);

            // Returns the path for a given data point.
            function path(d) {
                return line(dimensions.map(function(p) { return [x(p), y[p](d[p])]; }));
            }

            // Handles a brush event, toggling the display of foreground lines.
            function brush() {
                var actives = dimensions.filter(function(p) { return !y[p].brush.empty(); }),
                    extents = actives.map(function(p) { return y[p].brush.extent(); });
                // console.log(actives)
                // console.log(extents)
                foreground.style("display", function(d) {
                    return actives.every(function(p, i) {
                        return extents[i][0] <= d[p] && d[p] <= extents[i][1];
                    }) ? null : "none";
                });
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
            this.$axios.post('get_parcoords_data', d.algorithm)
            .then((res) => {
                d3.select('.par-coords').selectAll('*').remove();  // 移除原来的画布所画内容
                var data = res.data
                console.log("par_data", data);

                var seeds = [] // 获取最终的激活节点，传到Structure View
                data.forEach( d => {
                    seeds.push(d.name)
                } )
                this.$bus.$emit("final-nodes", seeds)

                // this.draw(data)

            })
            .catch((error) => {
                console.log('get_parcoords_data', error);
            })
        })

        var periodList = []
        this.$bus.$on("selected_period_included_vg", period_vg => {
            d3.selectAll(".foreground").attr("visibility", "hidden")

            if (periodList !== period_vg) {
                period_vg.forEach( d => {
                    d3.select("#vg-" + d.node).style("visibility", "visible")
                })
                console.log(period_vg)
                periodList.forEach( d => {
                    d3.select("#vg-" + d.node).style("visibility", "hidden")
                })
                console.log(periodList)
            }
            periodList = period_vg
        })

        this.$bus.$on("highlighted_vg-mouseover", d => {
            d3.select("#vg-" + d)
                // .style("stroke-dasharray", "blue")
                .style("stroke-width", 5)
        })
        this.$bus.$on("highlighted_vg-mouseout", d => {
            // var color = document.defaultView.getComputedStyle(document.getElementById("vg-" + d), null) //获取style属性
            // var col = color.stroke

            // console.log(color)
            // console.log(col)
            d3.select("#vg-" + d)
                // .style("stroke", "steelblue")
                .style("stroke-width", 2)
        })
    }
}
</script>
<style>

    svg {
      font: 10px sans-serif;
    }

    .background path {
      fill: none;
      stroke: #ddd;
      shape-rendering: crispEdges;
    }

    .foreground path {
      fill: none;
      /*stroke: steelblue;*/
    }

    .brush .extent {
      fill-opacity: .3;
      stroke: #fff;
      shape-rendering: crispEdges;
    }

    .axis-par line,
    .axis-par path {
      fill: none;
      stroke: #000;
      shape-rendering: crispEdges;
    }

    .axis-par text {
      text-shadow: 0 1px 0 #fff, 1px 0 0 #fff, 0 -1px 0 #fff, -1px 0 0 #fff;
    }

</style>