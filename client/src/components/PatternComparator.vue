<template>
    <div class='pattern-comparator' ref='root'>
    </div>
</template>

<script>
import * as d3 from '../assets/js/d3/d3.v3.js'
// import '../assets/js/d3/d3.tip.js'
// import {loadLiquidFillGauge} from '../assets/js/d3/liquidFillGauge.js'
// import {liquidFillGaugeDefaultSettings} from '../assets/js/d3/liquidFillGauge.js'


export default{
    name:'PatternComparator',
    data(){
        return{

        }

    },
    props:[],
    methods:{
        draw_pattern(data){
            // SVG画布边缘与图表内容的距离
            var margin = {top: 10, right: 30, bottom: 30, left: 40},
                width = 296 - margin.left - margin.right,
                height = 460 - margin.top - margin.bottom
                // height = 654 - margin.top - margin.bottom

            // var cluster_color = ['#ebb0a4', "#84d9d4", "#d8b3e1", "#c4d4a3", "#93c1ed",'#FB5652','#FFB005']; //ori
            // var cluster_color = ['rgb(255, 208, 120)', "rgb(178, 224, 116)", "rgb(189, 217, 246)", "rgb(142, 155, 224)", "rgb(214, 76, 77)",'#FB5652','#FFB005']; //bus
            // var cluster_color = ['rgb(68, 140, 189)', "rgb(247, 147, 56)", "rgb(78, 173, 80)", "rgb(219, 122,111)", "rgb(161, 127, 196)",'#FB5652','#FFB005']; //DGS
            var cluster_color = ['rgb(27, 132, 199)', "rgb(63, 214, 214)", "rgb(255, 207, 80)", "rgb(255, 128,101)", "rgb(223, 159, 235)",'#FB5652','#FFB005']; //muluba

            var svg = d3.select('.pattern-comparator').append('svg')
                .attr('width', width + margin.left + margin.right)
                .attr('height', height + margin.top + margin.bottom)
                .attr("transform", "translate(0," + 5 + ")")
                // .attr('transform', 'translate(' + margin.right + ',' + margin.top + ')')

            var pat_g = svg.append("g")
                .attr("class", "algorithm")
                .attr('transform', 'translate(' + margin.right + ',' + margin.top*2.5 + ')')

            var algorithm_svg = pat_g.selectAll("g")
                .data(data)
                .enter().append("g")
                .attr("id", d => 'algorithm_group-'+ d.algorithm )
                .attr("transform", function (d, i) {
                    return "translate(" + (i * 100)  + ",0)";
                })
            console.log(data)

            var patPadding = 34

            var pie_svg = algorithm_svg.selectAll(".pie")
            // algorithm_svg.selectAll(".pie")
                .data(d => d.value)
                .enter().append("g")
                .attr("class", "pie")
                .attr("id", d => 'pattern_group-'+ d.pattern )
                .attr("transform", function (d, i) {
                    return "translate(0," + (i * patPadding)  + ")";
                })

            var line_g = svg.append("g")
                        .attr("class", "line")
                        .attr('transform', 'translate(0' + ',' + 8 + ')')

            line_g.selectAll("line")
                .data(data[0]["value"])
                .enter().append("line")
                .attr("class", "axis-line")
                .attr("id", d => 'line_group-'+ d.pattern )
                .attr("x1", "0")
                .attr("y1", function (d, i) {
                    return parseFloat((i+1) * (patPadding));
                })
                .attr('x2', width + margin.left + margin.right)
                .attr("y2", function (d, i) {
                    return parseFloat((i+1) * (patPadding));
                })
                .style("stroke", "#e5e5e7")
                .style("stroke-width", "2")

            // 样式小图
            pie_svg.selectAll(".pat")
                .data(d => d.value)
                .enter().append("g")
                .attr("class", "pat")
                .attr("id", d => 'pie_group-'+ d.id )
                .each(draw_glyph)
                .select("g")

            function draw_glyph(d, i){
                data = d.value
                // console.log("data", data)
            // SVG画布边缘与图表内容的距离
            var margin = {top: 10, right: 20, bottom: 20, left: 30},
                width = 240 - margin.left - margin.right,
                height = 135 - margin.top - margin.bottom
            // var svg = d3.select('.pattern-comparator').append('svg')
            //     .attr('width', width + margin.left + margin.right)
            //     .attr('height', height + margin.top + margin.bottom)
            //     .append('g')
            //     .attr('transform','translate(' + width / 2 + ',' + height / 2 + ')')

            var svg = d3.select(this)
                    .attr('width', width + margin.left + margin.right)
                    .attr('height', height + margin.top + margin.bottom)
                    .append("g")
                    .attr("transform",  "translate(" + (i * patPadding)  + ",0)")


            var radius = Math.min(width, height) / 7,
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


            // console.log(pie(data))

            // var outerPath = svg.selectAll(".outlineArc")
            svg.selectAll(".outlineArc")
                .data(pie(data))
                .enter().append("path")
                .attr("fill", "none")
                .attr("stroke", "gray")
                .attr("class", "outlineArc")
                .attr("d", outlineArc)
                .style("opacity", 0.2)


            // // calculate the weighted mean score
            // var score =
            //     data.reduce(function(a, b) {
            //         //console.log('a:' + a + ', b.score: ' + b.score + ', b.weight: ' + b.weight);
            //         return a + (b.score * b.weight);
            //     }, 0) /
            //     data.reduce(function(a, b) {
            //         return a + b.weight;
            //     }, 0);
            //
            var z = d3.scale.ordinal()
            // .range(['#CCCE70', "#98D1C8", "#EDCC63", "#F6F5B3", "#F4D3C1",'#FB5652','#FFB005'])
                .range(cluster_color);

            z.domain(["4", "3", "2", "1", "0"]);

            svg
                // .selectAll("circle")
                // .data(data)
                // .enter()
                .append("circle")
                .attr("class", "pat-circle")
                .attr("r", "3.5")
                .attr("fill", z(d.id))
                // .attr("text-anchor", "middle") // text-align: right
                // .text(d.id)
                // .style("visibility", "hidden");


            // // draw liquidFillGauge
            // var g_liquid = svg
            //     .append("g")
            //     .attr('height', "43")  // 给的是style不是dom属性的attr
            //     .attr('width',"97%")
            //     .attr("id", "fillgauge")
            //     // .on("click", gauge.update(NewValue()))
            //     .attr('transform','translate('+ (-get_dis()) + ','+ (-get_dis()) +')');
            //
            // function get_dis() { // 给到liquid的position
            //     var dis = Math.min(parseInt(d3.select("#fillgauge").attr("width")), parseInt(d3.select("#fillgauge").attr("height"))) / 2
            //     return dis
            // }
            //
            // g_liquid.onclick = function () {gauge.update(NewValue());}  // 调用的是dom-svg的
            //
            // var gauge = loadLiquidFillGauge("fillgauge", 35);
            //
            //
            // function NewValue(){
            //     if(Math.random() > .5){
            //         return Math.round(Math.random()*100);
            //     } else {
            //         return (Math.random()*100).toFixed(1);
            //     }
            // }


            // function liquidFillGaugeDefaultSettings(){
            //     return {
            //         minValue: 0, // The gauge minimum value.
            //         maxValue: 100, // The gauge maximum value.
            //         circleThickness: 0.05, // The outer circle thickness as a percentage of it's radius.
            //         circleFillGap: 0.05, // The size of the gap between the outer circle and wave circle as a percentage of the outer circles radius.
            //         circleColor: "#178BCA", // The color of the outer circle.
            //         waveHeight: 0.05, // The wave height as a percentage of the radius of the wave circle.
            //         waveCount: 1, // The number of full waves per width of the wave circle.
            //         waveRiseTime: 1000, // The amount of time in milliseconds for the wave to rise from 0 to it's final height.
            //         waveAnimateTime: 1000, // The amount of time in milliseconds for a full wave to enter the wave circle.
            //         waveRise: true, // Control if the wave should rise from 0 to it's full height, or start at it's full height.
            //         waveHeightScaling: true, // Controls wave size scaling at low and high fill percentages. When true, wave height reaches it's maximum at 50% fill, and minimum at 0% and 100% fill. This helps to prevent the wave from making the wave circle from appear totally full or empty when near it's minimum or maximum fill.
            //         waveAnimate: true, // Controls if the wave scrolls or is static.
            //         waveColor: "#178BCA", // The color of the fill wave.
            //         waveOffset: 0, // The amount to initially offset the wave. 0 = no offset. 1 = offset of one full wave.
            //         textVertPosition: .5, // The height at which to display the percentage text withing the wave circle. 0 = bottom, 1 = top.
            //         textSize: 1, // The relative height of the text to display in the wave circle. 1 = 50%
            //         valueCountUp: true, // If true, the displayed value counts up from 0 to it's final value upon loading. If false, the final value is displayed.
            //         displayPercent: true, // If true, a % symbol is displayed after the value.
            //         textColor: "#045681", // The color of the value text when the wave does not overlap it.
            //         waveTextColor: "#A4DBf8" // The color of the value text when the wave overlaps it.
            //     };
            // }

            // function loadLiquidFillGauge(elementId, value, config) {
            //     if(config == null) config = liquidFillGaugeDefaultSettings();
            //
            //     var gauge = d3.select("#" + elementId);
            //     var radius = Math.min(parseInt(gauge.attr("width")), parseInt(gauge.attr("height")))/2;
            //     // var locationX = parseInt(gauge.attr("width"))/2 - radius;
            //     // var locationY = parseInt(gauge.attr("height"))/2 - radius;
            //     var fillPercent = Math.max(config.minValue, Math.min(config.maxValue, value))/config.maxValue;
            //
            //     var waveHeightScale;
            //     if(config.waveHeightScaling){
            //         waveHeightScale = d3.scale.linear()
            //             .range([0,config.waveHeight,0])
            //             .domain([0,50,100]);
            //     } else {
            //         waveHeightScale = d3.scale.linear()
            //             .range([config.waveHeight,config.waveHeight])
            //             .domain([0,100]);
            //     }
            //
            //     var textPixels = (config.textSize*radius/2);
            //     var textFinalValue = parseFloat(value).toFixed(2);
            //     var textStartValue = config.valueCountUp?config.minValue:textFinalValue;
            //     var percentText = config.displayPercent?"%":"";
            //     var circleThickness = config.circleThickness * radius;
            //     var circleFillGap = config.circleFillGap * radius;
            //     var fillCircleMargin = circleThickness + circleFillGap;
            //     var fillCircleRadius = radius - fillCircleMargin;
            //     var waveHeight = fillCircleRadius*waveHeightScale(fillPercent*100);
            //
            //     var waveLength = fillCircleRadius*2/config.waveCount;
            //     var waveClipCount = 1+config.waveCount;
            //     var waveClipWidth = waveLength*waveClipCount;
            //
            //     // Rounding functions so that the correct number of decimal places is always displayed as the value counts up.
            //     var textRounder = function(value){ return Math.round(value); };
            //     if(parseFloat(textFinalValue) !== parseFloat(textRounder(textFinalValue))){
            //         textRounder = function(value){ return parseFloat(value).toFixed(1); };
            //     }
            //     if(parseFloat(textFinalValue) !== parseFloat(textRounder(textFinalValue))){
            //         textRounder = function(value){ return parseFloat(value).toFixed(2); };
            //     }
            //
            //     // Data for building the clip wave area.
            //     var data = [];
            //     for(var i = 0; i <= 40*waveClipCount; i++){
            //         data.push({x: i/(40*waveClipCount), y: (i/(40))});
            //     }
            //
            //     // Scales for drawing the outer circle.
            //     var gaugeCircleX = d3.scale.linear().range([0,2*Math.PI]).domain([0,1]);
            //     var gaugeCircleY = d3.scale.linear().range([0,radius]).domain([0,radius]);
            //
            //     // Scales for controlling the size of the clipping path.
            //     var waveScaleX = d3.scale.linear().range([0,waveClipWidth]).domain([0,1]);
            //     var waveScaleY = d3.scale.linear().range([0,waveHeight]).domain([0,1]);
            //
            //     // Scales for controlling the position of the clipping path.
            //     var waveRiseScale = d3.scale.linear()
            //         // The clipping area size is the height of the fill circle + the wave height, so we position the clip wave
            //         // such that the it will overlap the fill circle at all when at 0%, and will totally cover the fill
            //         // circle at 100%.
            //         .range([(fillCircleMargin+fillCircleRadius*2+waveHeight),(fillCircleMargin-waveHeight)])
            //         .domain([0,1]);
            //     var waveAnimateScale = d3.scale.linear()
            //         .range([0, waveClipWidth-fillCircleRadius*2]) // Push the clip area one full wave then snap back.
            //         .domain([0,1]);
            //
            //     // Scale for controlling the position of the text within the gauge.
            //     var textRiseScaleY = d3.scale.linear()
            //         .range([fillCircleMargin+fillCircleRadius*2,(fillCircleMargin+textPixels*0.7)])
            //         .domain([0,1]);
            //
            //     // Center the gauge within the parent SVG.
            //     var gaugeGroup = gauge.append("g")
            //
            //         // .attr('transform','translate('+locationX+','+locationY+')');
            //
            //     // Draw the outer circle.
            //     var gaugeCircleArc = d3.svg.arc()
            //         .startAngle(gaugeCircleX(0))
            //         .endAngle(gaugeCircleX(1))
            //         .outerRadius(gaugeCircleY(radius))
            //         .innerRadius(gaugeCircleY(radius-circleThickness));
            //     gaugeGroup.append("path")
            //         .attr("d", gaugeCircleArc)
            //         .style("fill", config.circleColor)
            //         .attr('transform','translate('+radius+','+radius+')');
            //
            //     // Text where the wave does not overlap.
            //     var text1 = gaugeGroup.append("text")
            //         .text(textRounder(textStartValue) + percentText)
            //         .attr("class", "liquidFillGaugeText")
            //         .attr("text-anchor", "middle")
            //         .attr("font-size", textPixels + "px")
            //         .style("fill", config.textColor)
            //         .attr('transform','translate('+radius+','+textRiseScaleY(config.textVertPosition)+')');
            //
            //     // The clipping wave area.
            //     var clipArea = d3.svg.area()
            //         .x(function(d) { return waveScaleX(d.x); } )
            //         .y0(function(d) { return waveScaleY(Math.sin(Math.PI*2*config.waveOffset*-1 + Math.PI*2*(1-config.waveCount) + d.y*2*Math.PI));} )
            //         .y1(function() { return (fillCircleRadius*2 + waveHeight); } );
            //     var waveGroup = gaugeGroup.append("defs")
            //         .append("clipPath")
            //         .attr("id", "clipWave" + elementId);
            //     var wave = waveGroup.append("path")
            //         .datum(data)
            //         .attr("d", clipArea)
            //         .attr("T", 0);
            //
            //     // The inner circle with the clipping wave attached.
            //     var fillCircleGroup = gaugeGroup.append("g")
            //         .attr("clip-path", "url(#clipWave" + elementId + ")");
            //     fillCircleGroup.append("circle")
            //         .attr("cx", radius)
            //         .attr("cy", radius)
            //         .attr("r", fillCircleRadius)
            //         .style("fill", config.waveColor);
            //
            //     // Text where the wave does overlap.
            //     var text2 = fillCircleGroup.append("text")
            //         .text(textRounder(textStartValue) + percentText)
            //         .attr("class", "liquidFillGaugeText")
            //         .attr("text-anchor", "middle")
            //         .attr("font-size", textPixels + "px")
            //         .style("fill", config.waveTextColor)
            //         .attr('transform','translate('+radius+','+textRiseScaleY(config.textVertPosition)+')');
            //
            //     // Make the value count up.
            //     if(config.valueCountUp){
            //         var textTween = function(){
            //             var i = d3.interpolate(this.textContent, textFinalValue);
            //             return function(t) { this.textContent = textRounder(i(t)) + percentText; }
            //         };
            //         text1.transition()
            //             .duration(config.waveRiseTime)
            //             .tween("text", textTween);
            //         text2.transition()
            //             .duration(config.waveRiseTime)
            //             .tween("text", textTween);
            //     }
            //
            //     // Make the wave rise. wave and waveGroup are separate so that horizontal and vertical movement can be controlled independently.
            //     var waveGroupXPosition = fillCircleMargin+fillCircleRadius*2-waveClipWidth;
            //     if(config.waveRise){
            //         waveGroup.attr('transform','translate('+waveGroupXPosition+','+waveRiseScale(0)+')')
            //             .transition()
            //             .duration(config.waveRiseTime)
            //             .attr('transform','translate('+waveGroupXPosition+','+waveRiseScale(fillPercent)+')')
            //             .each("start", function(){ wave.attr('transform','translate(1,0)'); }); // This transform is necessary to get the clip wave positioned correctly when waveRise=true and waveAnimate=false. The wave will not position correctly without this, but it's not clear why this is actually necessary.
            //     } else {
            //         waveGroup.attr('transform','translate('+waveGroupXPosition+','+waveRiseScale(fillPercent)+')');
            //     }
            //
            //     if(config.waveAnimate) animateWave();
            //
            //     function animateWave() {
            //         wave.attr('transform','translate('+waveAnimateScale(wave.attr('T'))+',0)');
            //         wave.transition()
            //             .duration(config.waveAnimateTime * (1-wave.attr('T')))
            //             .ease('linear')
            //             .attr('transform','translate('+waveAnimateScale(1)+',0)')
            //             .attr('T', 1)
            //             .each('end', function(){
            //                 wave.attr('T', 0);
            //                 animateWave(config.waveAnimateTime);
            //             });
            //     }
            //
            //     function GaugeUpdater(){
            //         this.update = function(value){
            //             var newFinalValue = parseFloat(value).toFixed(2);
            //             var textRounderUpdater = function(value){ return Math.round(value); };
            //             if(parseFloat(newFinalValue) !== parseFloat(textRounderUpdater(newFinalValue))){
            //                 textRounderUpdater = function(value){ return parseFloat(value).toFixed(1); };
            //             }
            //             if(parseFloat(newFinalValue) !== parseFloat(textRounderUpdater(newFinalValue))){
            //                 textRounderUpdater = function(value){ return parseFloat(value).toFixed(2); };
            //             }
            //
            //             var textTween = function(){
            //                 var i = d3.interpolate(this.textContent, parseFloat(value).toFixed(2));
            //                 return function(t) { this.textContent = textRounderUpdater(i(t)) + percentText; }
            //             };
            //
            //             text1.transition()
            //                 .duration(config.waveRiseTime)
            //                 .tween("text", textTween);
            //             text2.transition()
            //                 .duration(config.waveRiseTime)
            //                 .tween("text", textTween);
            //
            //             var fillPercent = Math.max(config.minValue, Math.min(config.maxValue, value))/config.maxValue;
            //             var waveHeight = fillCircleRadius*waveHeightScale(fillPercent*100);
            //             var waveRiseScale = d3.scale.linear()
            //                 // The clipping area size is the height of the fill circle + the wave height, so we position the clip wave
            //                 // such that the it will overlap the fill circle at all when at 0%, and will totally cover the fill
            //                 // circle at 100%.
            //                 .range([(fillCircleMargin+fillCircleRadius*2+waveHeight),(fillCircleMargin-waveHeight)])
            //                 .domain([0,1]);
            //             var newHeight = waveRiseScale(fillPercent);
            //             var waveScaleX = d3.scale.linear().range([0,waveClipWidth]).domain([0,1]);
            //             var waveScaleY = d3.scale.linear().range([0,waveHeight]).domain([0,1]);
            //             var newClipArea;
            //             if(config.waveHeightScaling){
            //                 newClipArea = d3.svg.area()
            //                     .x(function(d) { return waveScaleX(d.x); } )
            //                     .y0(function(d) { return waveScaleY(Math.sin(Math.PI*2*config.waveOffset*-1 + Math.PI*2*(1-config.waveCount) + d.y*2*Math.PI));} )
            //                     .y1(function() { return (fillCircleRadius*2 + waveHeight); } );
            //             } else {
            //                 newClipArea = clipArea;
            //             }
            //
            //             var newWavePosition = config.waveAnimate?waveAnimateScale(1):0;
            //             wave.transition()
            //                 .duration(0)
            //                 .transition()
            //                 .duration(config.waveAnimate?(config.waveAnimateTime * (1-wave.attr('T'))):(config.waveRiseTime))
            //                 .ease('linear')
            //                 .attr('d', newClipArea)
            //                 .attr('transform','translate('+newWavePosition+',0)')
            //                 .attr('T','1')
            //                 .each("end", function(){
            //                     if(config.waveAnimate){
            //                         wave.attr('transform','translate('+waveAnimateScale(0)+',0)');
            //                         animateWave(config.waveAnimateTime);
            //                     }
            //                 });
            //             waveGroup.transition()
            //                 .duration(config.waveRiseTime)
            //                 .attr('transform','translate('+waveGroupXPosition+','+newHeight+')')
            //         }
            //     }
            //
            //     return new GaugeUpdater();
            // }


        }



        },



    },
    computed:{

    },
    watch:{

    },
    created(){

    },
    mounted(){
        // this.$axios.get('get_patcomptor_data')
        //     .then((res) =>{
        //         var data = res.data
        //         console.log(data)
        //         // this.draw_glyph(data)
        //         this.draw_pattern(data)
        //     })
        //     .catch((error) =>{
        //         console.log('get_patcomptor_data', error)
        //     })

        // 默认值
        this.$axios.post('get_patcomptor_data', "agr_1")
            .then((res) => {
                console.log(res)
                console.log(typeof res.data)
                d3.select('.pattern-comparator').selectAll('*').remove();  // 移除原来的画布所画内容
                var data = res.data
                console.log("pattern_data", data);
                this.$bus.$emit("default_Alg_A", data)
                this.draw_pattern(data)
                // this.draw(data);
            })
            .catch((error) => {
                console.log('get_patcomptor_data', error);
            })

        // 事件触发后->改变算法
        this.$bus.$on('algorithm-selected-hot', (d) => {
            console.log(d)
            this.$axios.post('get_patcomptor_data', d.algorithm)
            .then((res) => {
                d3.select('.pattern-comparator').selectAll('*').remove();  // 移除原来的画布所画内容
                var data = res.data
                console.log("pattern_data", data);
                this.$bus.$emit("click_Alg_A", data)
                this.draw_pattern(data)
                // this.draw(data);
            })
            .catch((error) => {
                console.log('get_patcomptor_data', error);
            })
        })

        // 事件触发后->改变算法
        this.$bus.$on('algorithm-selected-pat1', (d) => {
            console.log(d)
            this.$axios.post('get_patcomptor_data', d.algorithm)
            .then((res) => {
                d3.select('.pattern-comparator').selectAll('*').remove();  // 移除原来的画布所画内容
                var data = res.data
                console.log("pattern_data", data);
                this.$bus.$emit("selected-pat1_Alg_A", data)
                this.draw_pattern(data)
                // this.draw(data);
            })
            .catch((error) => {
                console.log('get_patcomptor_data', error);
            })
        })

        // 外圆环的线条不可见
        this.$bus.$on('switch-selected-pat', (d) => {
            if (d.value) return d3.selectAll(".outlineArc").style("visibility", "visible")
            else return d3.selectAll(".outlineArc").style("visibility", "hidden")
        })
    }
}
</script>

<style>

    .liquidFillGaugeText { font-family: Helvetica; font-weight: bold; }

    .axis path,
    .axis line {
      fill: none;
      stroke: #000;
      shape-rendering: crispEdges;
    }

    .bar {
      fill: orange;
    }

    .solidArc:hover {
      fill: orangered ;
    }

    .solidArc {
        -moz-transition: all 0.3s;
        -o-transition: all 0.3s;
        -webkit-transition: all 0.3s;
        transition: all 0.3s;
    }

    .x.axis path {
      display: none;
    }

    .aster-score {
      line-height: 1;
      font-weight: bold;
      font-size: 500%;
    }

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
</style>