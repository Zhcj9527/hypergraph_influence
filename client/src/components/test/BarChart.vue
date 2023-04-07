<template>
  <div class="bar-chart" ref="root">
  </div>
</template>

<script>
import * as d3 from 'd3'

export default {
  name: "component_name",
  data() {
    return {}
  },
  props: [],
  methods: {
    draw(data) {
      // set the dimensions and margins of the graph
      var margin = {top: 10, right: 30, bottom: 30, left: 60},
          width = 960 - margin.left - margin.right,
          height = 600 - margin.top - margin.bottom
      // append the svg object to the body of the page
      var svg = d3.select('.bar-chart').append('svg')
          .attr('width', width + margin.left + margin.right).attr('height', height + margin.top + margin.bottom )
          .append('g')
          // .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')

      // var vm = this

      // X axis
      var x = d3.scaleBand()
          .domain(data.map(function (d) {
            return d.id;
          }))
          .range([0, width])
          .padding(0.3)

      svg.append('g')
          .attr('transform', 'translate(0,' + height + ')')
          .call(d3.axisBottom(x).tickSize(5))

      // Add Y axis
      var y = d3.scaleLinear()
          .domain([0, d3.max(data, function (d) {
            return d.value
          })])
          .range([height, 0])

      svg.append('g')
          .call(d3.axisLeft(y))
          .style("visibility", "hidden");

      // Bars
      svg.selectAll('rect')
          .data(data)
          .enter()
          .append('rect')//利用enter 创建与数据个数一样的rect矩形
          .attr("x", function (d) {
            return x(d.id);
          })
          .attr("y", function (d) {
            return y(d.value);
          })
          .attr("width", x.bandwidth())
          .attr("height", function (d) {
            return height - y(d.value);
          })
          .attr("fill", "#69b3a2")
          // .on('click', (d) => {
          //   if (d.x === 'China') {
          //     vm.$bus.$emit('China-selected', d.x)
          //   } else if (d.x === 'USA') {
          //     vm.$bus.$emit('USA-selected', d.x)
          //   } else {
          //     vm.$bus.$emit('Japan-selected', d.x)
          //   }
          // })

    }

  },
  computed: {},
  watch: {},
  created() {
  },
  mounted() {
    this.$axios.get('get_BarChart_data')
        .then((res) => {
          var data = res.data
          console.log("BarChart_data", data)
          this.draw(data)
        })
        .catch((error) => {
          console.log('get_BarChart_data', error)
        })
  }
}
</script>

<style scoped>

</style>
