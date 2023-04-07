<template>
    <div class='alg-line' ref='root'>
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
            var date_arr = data[0].values
            var margin = {top: 10, right: 30, bottom: 30, left: 60},
                width = 960 - margin.left - margin.right,
                height = 540 - margin.top - margin.bottom
            var svg = d3.select('.alg-line').append('svg')
                .attr('width', 960).attr('height', 540)
                .append('g')
                // .attr('transform','translate(' + margin.left + ',' + margin.top + ')')

            var x = d3.scaleBand()
                .domain(date_arr.map(function (d) {
                    return d.name;
                }))
                .range([0, width])
                .padding(0.1)

            const xaxis = d3.axisBottom(x)
                .tickValues(x.domain().filter(function(d,i){ return !(i%1)}));//日期每隔30个显示一次日期

            svg.append('g')
                .attr('transform','translate(0, ' + height + ')')
                .call(xaxis)


            // y轴
            var y = d3.scaleLinear()
                .domain([
                    d3.min(data, function(c) { return d3.min(c.values, function(d) { return d.value; }); }),
                    d3.max(data, function(c) { return d3.max(c.values, function(d) { return d.value; }); })
                ])
                .range([ height, 0 ])

            const yaxis = d3.axisLeft(y)
                .ticks(6)  // 控制坐标轴上的刻度个数
                //.tickSize(10) //控制刻度的大小
                //.tickPadding(5) //设置标签数字与坐标轴的距离
                //.tickFormat(d3.format(".0%")) //设置标签数字的格式
            svg.append('g')
                .call(yaxis)
                .style("visibility", "hidden");


            // var z = d3.scaleOrdinal(d3.schemeCategory10)
            //     .domain(data.map(function(c) { return c.id; }));


            // 颜色编码
            // var color = {
            //     "ETF0" : "#000000",
            //     "ETF1" : "#00008B",
            //     "ETF2" : "#0000FF",
            //     "ETF3" : "#008000",
            //     "ETF4" : "#008080",
            //     "ETF5" : "#00BFFF",
            //     "ETF6" : "#00CED1",
            //     "ETF7" : "#00FF00",
            //     "ETF8" : "#800000",
            //     "ETF9" : "#800080",
            //     "ETF10" : "#808000",
            //     "ETF11" : "#90EE90",
            //     "ETF12" : "#FF0000",
            //     "ETF13" : "#FF6347",
            //     "ETF14" : "#FFD700",
            //     "ETF15" : "#FFFF00",
            //
            // };

            // 折线
            var line = d3.line()
                .curve(d3.curveBasis)
                .x(function(d) { return x(d.name); })
                .y(function(d) { return y(d.value); })

            var stock = svg.selectAll(".stock")
                .data(data)
                .enter().append("g")
                .attr('class', 'stock')

            stock.append("path")
                .attr("transform", "translate(" + margin.left / 3 + ","  + 0 + ")")
                // .attr("transform", "translate(" + 0 + ","  + 0 + ")")
                .attr("d", function(d) { return line(d.values); })
                // .style("stroke", function(d) { return z(d.id); })
                .style("stroke", d => {
                    if ( d.id === "agr_3" || d.id === "agr_4" || d.id === "agr_5" ) {
                        return "#FFFF00"
                    } else if (d.id === "agr_1" || d.id === "agr_6" || d.id === "agr_7") {
                        return "#00008B"
                    // } else if (d.id === "agr_2") {
                    //     return "#0000FF"
                    // } else if (d.id === "agr_7" || d.id === "agr_8") {
                    //     return "#008000"
                    } else if (d.id === "agr_2" || d.id === "agr_8") {
                        return "#008000"
                    }})
                .attr('fill', 'none')
                // .attr('stroke-width', function(d) { return 10 * d.weight; })

            //各个股票的文本值，需要时再修改！！
            stock.append("text")
                .datum(function(d) { return {id: d.id, value: d.values[d.values.length - 1]}; })
                .attr("transform", function(d) { return "translate(" + x(d.value.name) + "," + y(d.value.value) + ")"; })
                .attr("x", 3)
                .attr("dy", "0.5em")
                .style("font", "10px sans-serif")
                .text(function(d) { return d.id; });


        }
    },
    computed:{

    },
    watch:{

    },
    //created(){

    //},
    mounted(){
        this.$axios.get('get_ETF_data')
            .then((res) =>{
                let data = res.data
                //let vm = this
                console.log("algLines_data", data)
                this.draw(data)
            })
            .catch((error) =>{
                console.log('ETF_data', error)
            })

    },
}
</script>

<style>

</style>