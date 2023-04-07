<template>
    <div class='plot-box' ref='root'>
    </div>
</template>

<script>
import * as d3 from '../assets/js/d3/d3'

export default{
    name:'PlotBox',
    data(){
        return{

        }
    },
    props:[],
    methods:{
        draw(data){
            var margin = {top: 10, right: 20, bottom: 10, left: 21},
                width = 427 - margin.left - margin.right,
                height = 508 - margin.top - margin.bottom;

            var cluster_num = 5
            // var patPadding = 34

            var svg = d3.select('.plot-box').append('svg')
                .attr('width', width + margin.left + margin.right)
                .attr('height', height + margin.top + margin.bottom)
                .append('g')
                .attr('transform','translate(' + margin.left + ',' + margin.bottom + ')');

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

            // 盒须图
            box_svg.selectAll(".pat")
                .data(d => d['box_data'])
                .enter().append("g")
                .attr("class", "pat")
                .attr("id", d => 'pie_group-'+ d.id )
                .each(draw_glyph)
                .select("g")

            // 盒须图
            function draw_glyph(d) {
                var dataset = d
                // console.log(d)
                const dms = {
                  width: 427,
                  height: 100,
                  margin: {
                    top: 10,
                    right: 10,
                    bottom: 20,
                    left: 20
                  },
                  tooltipMargin: 10
                }

                dms.innerWidth = dms.width - dms.margin.left - dms.margin.right;
                dms.innerHeight = dms.height - dms.margin.top - dms.margin.bottom;

                const colors = ["#9E0041", "#C32F4B", "#E1514B", "#F47245", "#FB9F59", "#FEC574", "#FAE38C", "#EAF195", "#C7E89E", "#9CD6A4", "#6CC4A4",
                    "#4D9DB4", "#4776B4", "#5E4EA1"]
                const Tooltip = d3.select('#tooltip')
                  .style('opacity', 0)
                  .style("background", "white")
                  .style("border", "1px solid #ddd")
                  .style("box-shadow", "2px 2px 3px 0px rgb(92 92 92 / 0.5)")
                  .style("font-size", ".8rem")
                  .style("padding", "2px 8px")
                  .style('font-weight', 600)
                  .style('position', 'absolute')

                // 排序
                dataset.sort((a, b) => a.value - b.value);
                // 获取值
                const yearAccessor = d => d.x;
                const yAccessor = d => d.y;
                const groupAccessor = d => d.value;

                // 分组
                const dataByYearAndGroup = d3.nest()
                  .key(yearAccessor)
                  .key(groupAccessor)
                  .entries(dataset)

                dataByYearAndGroup.forEach( (d, i) => {
                    d['values'][0]['color'] = colors[i]
                })

                // console.log(dataByYearAndGroup)

                // 计算箱线图所需要的最大值、最小值、中位数以及上下四分位数，还有离散值
                const dataByYearAndGroupWithStats = dataByYearAndGroup.map(year => {
                  const yearData = year['values'].map(group => {
                    const groupYValues = group.values.map(yAccessor).sort((a, b) => a - b)
                    const q1 = d3.quantile(groupYValues, 0.25)
                    const median = d3.median(groupYValues)
                    const q3 = d3.quantile(groupYValues, 0.75)
                    const iqr = q3 - q1
                    const [min, max] = d3.extent(groupYValues)
                    const rangeMin = d3.max([min, q1 - iqr * 1.5])
                    const rangeMax = d3.min([max, q3 + iqr * 1.5])
                    const outliers = group.values.filter(d => yAccessor(d) < rangeMin || yAccessor(d) > rangeMax)
                    return {
                      ...group,
                      month: +group.key,
                      q1, median, q3, iqr, min, max, rangeMin, rangeMax, outliers
                    }
                  })
                  return {
                    ...year,
                    values: yearData,
                  }
                });

                // draw canvas
                // <div class="group-box-plot" id="group-box-plot"></div>
                // <div id="tooltip"></div>
                const mainsvg = d3.select(this)
                  .append('svg')
                  .attr('width', dms.width)
                  .attr('height', dms.height)
                const maingroup = mainsvg.append('g')
                  .attr('transform', `translate(${dms.margin.left}, ${dms.margin.top})`)
                const boxArea = maingroup.append('g')

                // 一级分组
                const xScale = d3.scaleBand()
                  .domain(dataByYearAndGroupWithStats.map(d => d.key))
                  .rangeRound([0, dms.innerWidth])
                  .paddingInner(0.1)
                  .paddingOuter(.4)
                // 二级分组
                const groupScale = d3.scaleBand()
                  .padding(1.9)
                const groupKeys = dataByYearAndGroup[0]['values']
                  .map(d => { return d.key })
                // console.log(groupKeys)
                groupScale.domain(groupKeys).rangeRound([0, xScale.bandwidth()])
                const yScale = d3.scaleLinear()
                  .domain([d3.min(dataset, d => d.y) - 0.1, d3.max(dataset, d => d.y)])
                  .range([dms.innerHeight, 0])

                // 颜色
                const colorScale = d3.scaleOrdinal()
                  .range(colors)

                // draw data
                let binGroups = boxArea.selectAll('bin')
                  .data(dataByYearAndGroupWithStats)

                binGroups.exit().remove()
                const newBinGroups = binGroups
                  .enter()
                  .append("g")
                  .attr("class", "bin")
                  .attr('transform', d => `translate(${xScale(d.key)}, 0)`)

                binGroups = newBinGroups.merge(binGroups)


                const boxWidth = 30, boxPadding = 6;

                // 添加绘制区域与悬浮提示
                const boxGroups = binGroups.selectAll('box').data(d => d.values)
                  .join('g')
                  .attr('class', 'box')
                  .on('mouseover', (event) => {
                    d3.select('#tooltip')
                      .style('opacity', 1)
                      .html(boxTooltip(event))
                  })
                  .on('mousemove', () => {
                    const event = d3.event;
                    // console.log(event.pageX, event.pageY)
                    Tooltip
                      .style('left', (event.pageX + dms.tooltipMargin) + 'px')
                      .style('top', (event.pageY + dms.tooltipMargin) + 'px')
                  })
                  .on('mouseout', () => {
                    d3.select('#tooltip').style('opacity', 0);
                  });


                // 垂直的线
                boxGroups.append('line')
                  .attr('class', 'line1')
                  .attr('x1', d => groupScale(d.key))
                  .attr('x2', d => groupScale(d.key))
                  .attr('y1', d => yScale(d.rangeMin))
                  .attr('y2', d => yScale(d.rangeMax))
                  .style('width', 40)
                  .attr('stroke', d => colorScale(d.color))
                  .attr("stroke-width", 2)

                // 矩形（箱线图）
                boxGroups.append('rect')
                  .attr('x', d => groupScale(d.key) - boxWidth / 2)
                  .attr('y', d => yScale(d.q3))
                  .attr('width', boxWidth)
                  .attr('height', d => yScale(d.q1) - yScale(d.q3))
                  .attr('fill', d => colorScale(d.color))

                // 中值线
                boxGroups.append('line')
                  .attr('class', 'median')
                  .attr('x1', d => groupScale(d.key) - boxWidth / 2)
                  .attr('x2', d => groupScale(d.key) + boxWidth / 2)
                  .attr('y1', d => yScale(d.median))
                  .attr('y2', d => yScale(d.median))
                  .attr("stroke", 'black')
                  .style("width", 40)
                  .attr("stroke-width", 2)
                  .attr('opacity', 0.3)

                // 最大垂直线两端横线
                boxGroups.append('line')
                  .attr('class', 'line')
                  .attr('x1', d => groupScale(d.key) - boxWidth / 2 + boxPadding)
                  .attr('x2', d => groupScale(d.key) + boxWidth / 2 - boxPadding)
                  .attr('y1', d => yScale(d.rangeMin))
                  .attr('y2', d => yScale(d.rangeMin))
                  .style("width", 40)
                  .attr('stroke', d => colorScale(d.color))
                  .attr("stroke-width", 2)

                boxGroups.append('line')
                  .attr('class', 'line')
                  .attr('x1', d => groupScale(d.key) - boxWidth / 2 + boxPadding)
                  .attr('x2', d => groupScale(d.key) + boxWidth / 2 - boxPadding)
                  .attr('y1', d => yScale(d.rangeMax))
                  .attr('y2', d => yScale(d.rangeMax))
                  .style("width", 40)
                  .attr('stroke', d => colorScale(d.color))
                  .attr("stroke-width", 2)

                // 离散点
                boxGroups.append('g')
                  .attr("transform", d => `translate(${groupScale(d.key)}, 0)`)
                  .selectAll('circle')
                  .data(d => d.outliers)
                  .join("circle")
                  .attr("class", "outlier")
                  .attr("cy", d => yScale(yAccessor(d)))
                  .attr("r", 0)
                  .attr('fill', '#ffffff')
                  .attr('stroke', 'black')

                //  设置y坐标轴
                const yAxis = d3.axisLeft(yScale)
                  .ticks(3)

                maingroup.append('g')
                  .attr('class', 'y-axis')
                  .call(yAxis)

                // // 添加y轴label
                // yAxisGroup.append('text')
                //   .attr('class', 'axis-label')
                //   .attr('transform', `rotate(-90)`)
                //   .attr('x', -dms.innerHeight / 3)
                //   .attr('y', -dms.margin.left + 10)
                //   .html("value")
                //   .attr('fill', 'black')
                //   .attr('font-size', '12px')
                // 设置x坐标轴
                const labels = dataByYearAndGroup.map(d => { return d.key });
                const xAxis = d3.axisBottom(xScale)
                  .tickFormat((d, i) => labels[i]);
                const xAxisGroup = maingroup.append('g')
                  .attr('class', 'x-axis')
                  .attr('transform', `translate(0, ${dms.innerHeight})`)
                  .call(xAxis)
                // 添加x轴label
                xAxisGroup.append('text')
                  .attr('class', 'axis-label')
                  .attr('x', dms.innerWidth / 2)
                  .attr('y', 40)
                  .html("Year")
                  .attr('fill', 'black')
                  .attr('font-size', '12px')


                // 添加图例
                const legend = maingroup.append('g')
                  .selectAll('g')
                  .data(dataByYearAndGroupWithStats[0].values)
                  .join('g')
                  .attr('class', 'legend')
                  .attr('transform', (d, i) => `translate(0, ${i * 22})`)

                legend.append('rect')
                  .attr('x', dms.innerWidth + 5)
                  .attr('width', 19)
                  .attr('height', 16)
                  .attr('fill', d => colorScale(d.color))

                legend.append('text')
                  .attr('x', dms.innerWidth + 28)
                  .attr('y', 8)
                  .attr("dy", "0.32em")
                  .text(d => d.key)

                function boxTooltip(d) {
                  return `
                    <span class="label">group</span>: ${d.key}<br>
                    <span class="label">max</span>: ${d.rangeMax}<br>
                    <span class="label">q1</span>: ${d.q1}<br>
                    <span class="label">median</span>: ${d.median}<br>
                    <span class="label">q3</span>: ${d.q3}<br>
                    <span class="label">min</span>: ${d.rangeMin}<br>
                   `
                }
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
