<template>
    <div class='line-chart' ref='root'>
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
            // SVG画布边缘与图表内容的距离
            var margin = {top: 10, right: 30, bottom: 30, left: 60},
                width = 600 - margin.left - margin.right,
                height = 600 - margin.top - margin.bottom
            var svg = d3.select('.line-chart').append('svg')
                .attr('width', 600).attr('height', 600)
                .append('g')
                .attr('transform','translate(' + margin.left + ',' + margin.top + ')')

            // x轴
            var x = d3.scaleLinear()
                .domain([0, d3.max(data, function(d) { return d.x })])
                .range([ 0, width])
            svg.append('g')
                .attr('transform','translate(0, ' + height + ')')
                .call(d3.axisBottom(x))


            // y轴
            var y = d3.scaleLinear()
                .domain([0, d3.max(data, function(d) { return d.y })])
                .range([ height, 0 ])
            svg.append('g')
                .call(d3.axisLeft(y))

            // 折线
            svg.append('path')
                .datum(data)
                .attr('fill', 'none')
                .attr('stroke', 'steelblue')
                .attr('stroke-width', 1.5)
                .attr('d', d3.line()
                    .x(function(d) { return x(d.x) })
                    .y(function(d) { return y(d.y) })
                )
                .attr('stroke-dasharray', "20,10,5,5,5,10")
        }

    },
    computed:{

    },
    watch:{

    },
    created(){

    },
    mounted(){
        this.$axios.get('get_data')
            .then((res) =>{
                var data = res.data
                console.log(data)
                this.draw(data)
            })
            .catch((error) =>{
                console.log('get_data', error)
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