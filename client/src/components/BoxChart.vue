<template>
    <div>
        <div class='box-chart' ref='root'></div>
        <PlotBox></PlotBox>
    </div>
</template>

<script>
import * as d3 from '../assets/js/d3/d3.v3.js'
import PlotBox from "./PlotBox"
// import box from  '../assets/js/d3/box'

export default{
    name:'component_name',
    data(){
        return{

        }
    },
    components: {
        PlotBox
    },
    props:[],
    methods:{
        draw(data){
            var margin = {top: 10, right: 20, bottom: 10, left: 21},
                width = 100 - margin.left - margin.right,
                height = 508 - margin.top - margin.bottom;

            var cluster_num = 5
            var patPadding = 34
            var cluster_color = ['rgb(27, 132, 199)', "rgb(63, 214, 214)", "rgb(255, 207, 80)", "rgb(255, 128,101)", "rgb(223, 159, 235)",'#FB5652','#FFB005']; //muluba

            var svg = d3.select('.box-chart').append('svg')
                .attr('width', width + margin.left + margin.right)
                .attr('height', height + margin.top + margin.bottom)
                .append('g')
                .attr('transform','translate(' + margin.left*2.4 + ',' + margin.bottom*6 + ')');

            var box_svg = svg.append("g")
                .attr("class", "box")
                .selectAll("g")
                .data(data)
                .enter().append("g")
                .attr("class", "pie")
                .attr("id", d => 'box_group-'+ d.id )
                .attr("transform", function (d, i) {
                    return "translate(0," + (i * (height/cluster_num)) + ")";
                })

            // 南丁格尔图
            box_svg.selectAll(".pat")
                .data(d => d.value)
                .enter().append("g")
                .attr("class", "pat")
                .attr("id", d => 'pie_group-'+ d.id )
                .each(draw_glyph)
                .select("g")

            function draw_glyph(d, i){
                    data = d['id_avg_index']
                    // console.log("data", data)
                // SVG画布边缘与图表内容的距离
                var margin = {top: 10, right: 20, bottom: 20, left: 30},
                    width = 240 - margin.left - margin.right,
                    height = 135 - margin.top - margin.bottom

                var svg = d3.select(this)
                        .attr('width', width + margin.left + margin.right)
                        .attr('height', height + margin.top + margin.bottom)
                        .append("g")
                        .attr("transform",  "translate(" + (i * patPadding)  + ",0)")


                var radius = Math.min(width, height) / 2.5, // 圆形的半径大小
                    innerRadius = 0.4 * radius;

                var pie = d3.layout.pie()
                    .sort(null)
                    .value(function(d) { return d.width; });

                var tip = d3.tip()
                    .attr('class', 'd3-tip')
                    .offset([0, 0])
                    .html(function(d) {
                        return d.data.label + ": <span style='color:orangered'>" + d.data.score + "</span>";
                    });

                var arc = d3.svg.arc()
                    .innerRadius(innerRadius)
                    .outerRadius(function (d) {
                        return (radius - innerRadius) * (d.data.score / 20) + innerRadius;
                    });

                var outlineArc = d3.svg.arc()
                    .innerRadius(innerRadius)
                    .outerRadius(radius);

                svg.call(tip);

                data.forEach(function(d) {
                    // d.id     =  d.id;
                    d.order  = +d.order;
                    // d.color  =  d.color;
                    d.weight = +d.weight;
                    d.score  = +d.score;
                    d.width  = +d.weight;
                    // d.label  =  d.label;
                });

                // var path = svg.selectAll(".solidArc")
                svg.selectAll(".solidArc")
                    .data(pie(data))
                    .enter().append("path")
                    .attr("fill", function(d) { return d.data.color; })
                    .attr("class", "solidArc")
                    // .attr("stroke", "gray") 已放到css来定义
                    .attr("d", arc)
                    .on('mouseover', tip.show)
                    .on('mouseout', tip.hide);


                // var outerPath = svg.selectAll(".outlineArc")
                svg.selectAll(".outlineArc")
                    .data(pie(data))
                    .enter().append("path")
                    .attr("fill", "none")
                    .attr("stroke", "gray")
                    .attr("class", "outlineArc")
                    .attr("d", outlineArc)
                    .style("opacity", 0.2)

                var z = d3.scale.ordinal()
                // .range(['#CCCE70', "#98D1C8", "#EDCC63", "#F6F5B3", "#F4D3C1",'#FB5652','#FFB005'])
                    .range(cluster_color);

                z.domain(["4", "3", "2", "1", "0"]);

                svg.append("circle")
                    .attr("class", "pat-circle")
                    .attr("r", "12")
                    .attr("fill", z(d.id))

            }

            // 盒须图
            // var min = Infinity,
            //     max = -Infinity;
            //
            // var chart = d3.box()
            //       .whiskers(iqr(1.5))
            //       .width(width/11)
            //       .height(84);
            //
            // chart.domain([min, max]);
            //
            // box_svg.append("g")
            //     .attr("class", "right")
            //     .selectAll("svg")
            //     .data(d => d['box_data'])
            //   .enter().append("svg")
            //     .attr("class", "right")
            //     .attr("width", (width-90)/11)
            //     .attr("height", 84)
            //   .append("g")
            //     .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
            //     .call(chart);
            //
            // // Returns a function to compute the interquartile range.
            //   function iqr(k) {
            //     return function(d) {
            //       var q1 = d.quartiles[0],
            //           q3 = d.quartiles[2],
            //           iqr = (q3 - q1) * k,
            //           i = -1,
            //           j = d.length;
            //       while (d[++i] < q1 - iqr);
            //       while (d[--j] > q3 + iqr);
            //       return [i, j];
            //     };
            //   }


        },

        // // 盒须图的js
        // box() {
        //   // Inspired by http://informationandvisualization.de/blog/box-plot
        //   d3.box = function() {
        //     var width = 1,
        //         height = 1,
        //         duration = 0,
        //         domain = null,
        //         value = Number,
        //         whiskers = boxWhiskers,
        //         quartiles = boxQuartiles,
        //         tickFormat = null;
        //
        //     // For each small multiple…
        //     function box(g) {
        //       g.each(function(d, i) {
        //         d = d.map(value).sort(d3.ascending);
        //         // console.log(value);
        //         console.log(d);
        //         var g = d3.select(this),
        //             n = d.length,
        //             min = d[0],
        //             max = d[n - 1];
        //
        //         // Compute quartiles. Must return exactly 3 elements.
        //         var quartileData = d.quartiles = quartiles(d);
        //
        //         // Compute whiskers. Must return exactly 2 elements, or null.
        //         var whiskerIndices = whiskers && whiskers.call(this, d, i),
        //             whiskerData = whiskerIndices && whiskerIndices.map(function(i) { return d[i]; });
        //
        //           console.log(whiskerData)
        //
        //         // Compute outliers. If no whiskers are specified, all data are "outliers".
        //         // We compute the outliers as indices, so that we can join across transitions!
        //         var outlierIndices = whiskerIndices
        //             ? d3.range(0, whiskerIndices[0]).concat(d3.range(whiskerIndices[1] + 1, n))
        //             : d3.range(n);
        //
        //         // Compute the new x-scale.
        //         var x1 = d3.scale.linear()
        //             .domain(domain && domain.call(this, d, i) || [min, max])
        //             .range([height, 0]);
        //
        //         // Retrieve the old x-scale, if this is an update.
        //         var x0 = this.__chart__ || d3.scale.linear()
        //             .domain([0, Infinity])
        //             .range(x1.range());
        //
        //         // console.log(x0);
        //
        //         // Stash the new scale.
        //         this.__chart__ = x1;
        //
        //         // Note: the box, median, and box tick elements are fixed in number,
        //         // so we only have to handle enter and update. In contrast, the outliers
        //         // and other elements are variable, so we need to exit them! Variable
        //         // elements also fade in and out.
        //
        //         // Update center line: the vertical line spanning the whiskers.
        //         var center = g.selectAll("line.center")
        //             .data(whiskerData ? [whiskerData] : []);
        //
        //         center.enter().insert("line", "rect")
        //             .attr("class", "center")
        //             .attr("x1", width / 2)
        //             .attr("y1", function(d) { return x0(d[0]); })
        //             .attr("x2", width / 2)
        //             .attr("y2", function(d) { return x0(d[1]); })
        //             .style("opacity", 1e-6)
        //           .transition()
        //             .duration(duration)
        //             .style("opacity", 1)
        //             .attr("y1", function(d) { return x1(d[0]); })
        //             .attr("y2", function(d) { return x1(d[1]); });
        //
        //         center.transition()
        //             .duration(duration)
        //             .style("opacity", 1)
        //             .attr("y1", function(d) { return x1(d[0]); })
        //             .attr("y2", function(d) { return x1(d[1]); });
        //
        //         center.exit().transition()
        //             .duration(duration)
        //             .style("opacity", 1e-6)
        //             .attr("y1", function(d) { return x1(d[0]); })
        //             .attr("y2", function(d) { return x1(d[1]); })
        //             .remove();
        //
        //         // Update innerquartile box.
        //         var box = g.selectAll("rect.box")
        //             .data([quartileData]);
        //
        //         box.enter().append("rect")
        //             .attr("class", "box")
        //             .attr("x", 0)
        //             .attr("y", function(d) { return x0(d[2]); })
        //             .attr("width", width)
        //             .attr("height", function(d) { return x0(d[0]) - x0(d[2]); })
        //             .attr('fill', 'skyblue')
        //           .transition()
        //             .duration(duration)
        //             .attr("y", function(d) { return x1(d[2]); })
        //             .attr("height", function(d) { return x1(d[0]) - x1(d[2]); });
        //
        //         box.transition()
        //             .duration(duration)
        //             .attr("y", function(d) { return x1(d[2]); })
        //             .attr("height", function(d) { return x1(d[0]) - x1(d[2]); });
        //
        //         // Update median line.
        //         var medianLine = g.selectAll("line.median")
        //             .data([quartileData[1]]);
        //
        //         medianLine.enter().append("line")
        //             .attr("class", "median")
        //             .attr("x1", 0)
        //             .attr("y1", x0)
        //             .attr("x2", width)
        //             .attr("y2", x0)
        //           .transition()
        //             .duration(duration)
        //             .attr("y1", x1)
        //             .attr("y2", x1);
        //
        //         medianLine.transition()
        //             .duration(duration)
        //             .attr("y1", x1)
        //             .attr("y2", x1);
        //
        //         // Update whiskers.
        //         var whisker = g.selectAll("line.whisker")
        //             .data(whiskerData || []);
        //
        //         whisker.enter().insert("line", "circle, text")
        //             .attr("class", "whisker")
        //             .attr("x1", 0)
        //             .attr("y1", x0)
        //             .attr("x2", width)
        //             .attr("y2", x0)
        //             .style("opacity", 1e-6)
        //           .transition()
        //             .duration(duration)
        //             .attr("y1", x1)
        //             .attr("y2", x1)
        //             .style("opacity", 1);
        //
        //         whisker.transition()
        //             .duration(duration)
        //             .attr("y1", x1)
        //             .attr("y2", x1)
        //             .style("opacity", 1);
        //
        //         whisker.exit().transition()
        //             .duration(duration)
        //             .attr("y1", x1)
        //             .attr("y2", x1)
        //             .style("opacity", 1e-6)
        //             .remove();
        //
        //         // Update outliers.
        //         var outlier = g.selectAll("circle.outlier")
        //             .data(outlierIndices, Number);
        //
        //         outlier.enter().insert("circle", "text")
        //             .attr("class", "outlier")
        //             .attr("r", 5)
        //             .attr("cx", width / 2)
        //             .attr("cy", function(i) { return x0(d[i]); })
        //             .style("opacity", 1e-6)
        //           .transition()
        //             .duration(duration)
        //             .attr("cy", function(i) { return x1(d[i]); })
        //             .style("opacity", 1);
        //
        //         outlier.transition()
        //             .duration(duration)
        //             .attr("cy", function(i) { return x1(d[i]); })
        //             .style("opacity", 1);
        //
        //         outlier.exit().transition()
        //             .duration(duration)
        //             .attr("cy", function(i) { return x1(d[i]); })
        //             .style("opacity", 1e-6)
        //             .remove();
        //
        //         // Compute the tick format.
        //         var format = tickFormat || x1.tickFormat(8);
        //
        //         // Update box ticks.
        //         var boxTick = g.selectAll("text.box")
        //             .data(quartileData);
        //
        //         boxTick.enter().append("text")
        //             .attr("class", "box")
        //             .attr("dy", ".3em")
        //             .attr("dx", function(d, i) { return i & 1 ? 6 : -6 })
        //             .attr("x", function(d, i) { return i & 1 ? width : 0 })
        //             .attr("y", x0)
        //             .attr("text-anchor", function(d, i) { return i & 1 ? "start" : "end"; })
        //             .text(format)
        //           .transition()
        //             .duration(duration)
        //             .attr("y", x1);
        //
        //         boxTick.transition()
        //             .duration(duration)
        //             .text(format)
        //             .attr("y", x1);
        //
        //         // Update whisker ticks. These are handled separately from the box
        //         // ticks because they may or may not exist, and we want don't want
        //         // to join box ticks pre-transition with whisker ticks post-.
        //         var whiskerTick = g.selectAll("text.whisker")
        //             .data(whiskerData || []);
        //
        //         whiskerTick.enter().append("text")
        //             .attr("class", "whisker")
        //             .attr("dy", ".3em")
        //             .attr("dx", 6)
        //             .attr("x", width)
        //             .attr("y", x0)
        //             .text(format)
        //             .style("opacity", 1e-6)
        //           .transition()
        //             .duration(duration)
        //             .attr("y", x1)
        //             .style("opacity", 1);
        //
        //         whiskerTick.transition()
        //             .duration(duration)
        //             .text(format)
        //             .attr("y", x1)
        //             .style("opacity", 1);
        //
        //         whiskerTick.exit().transition()
        //             .duration(duration)
        //             .attr("y", x1)
        //             .style("opacity", 1e-6)
        //             .remove();
        //       });
        //         d3.timer.flush();
        //     }
        //
        //     box.width = function(x) {
        //       if (!arguments.length) return width;
        //       width = x;
        //       return box;
        //     };
        //
        //     box.height = function(x) {
        //       if (!arguments.length) return height;
        //       height = x;
        //       return box;
        //     };
        //
        //     box.tickFormat = function(x) {
        //       if (!arguments.length) return tickFormat;
        //       tickFormat = x;
        //       return box;
        //     };
        //
        //     box.duration = function(x) {
        //       if (!arguments.length) return duration;
        //       duration = x;
        //       return box;
        //     };
        //
        //     box.domain = function(x) {
        //       if (!arguments.length) return domain;
        //       domain = x == null ? x : d3.functor(x);
        //       return box;
        //     };
        //
        //     box.value = function(x) {
        //       if (!arguments.length) return value;
        //       value = x;
        //       return box;
        //     };
        //
        //     box.whiskers = function(x) {
        //       if (!arguments.length) return whiskers;
        //       whiskers = x;
        //       return box;
        //     };
        //
        //     box.quartiles = function(x) {
        //       if (!arguments.length) return quartiles;
        //       quartiles = x;
        //       return box;
        //     };
        //
        //     return box;
        //   };
        //
        //   function boxWhiskers(d) {
        //     return [0, d.length - 1];
        //   }
        //
        //   function boxQuartiles(d) {
        //     return [
        //       d3.quantile(d, .25),
        //       d3.quantile(d, .5),
        //       d3.quantile(d, .75)
        //     ];
        //   }
        // }

    },
    computed:{

    },
    watch:{

    },
    created(){

    },
    mounted(){
        this.$axios.get('get_box_data')
        .then((res) =>{
            var data = res.data
            console.log(data)
            this.draw(data)
        })
        .catch((error) =>{
            console.log('get_box_data', error)
        })
        // this.$bus.$on('algorithm-selected-hot', (d) => {
        //     console.log(d)
        //     this.$axios.post('get_scatter_data', d.algorithm)
        //     .then((res) => {
        //         d3.select('.scatter-chart').selectAll('*').remove();  // 移除原来的画布所画内容
        //         var data = res.data
        //         console.log("scatter_data", data);
        //
        //         var seeds = [] // 获取最终的激活节点，传到Structure View
        //         data.forEach( d => {
        //             seeds.push(d.name)
        //         } )
        //         this.$bus.$emit("final-nodes", seeds)
        //
        //         this.draw(data)
        //
        //     })
        //     .catch((error) => {
        //         console.log('get_scatter-chart', error);
        //     })
        // })

    }
}
</script>

<style>

</style>
