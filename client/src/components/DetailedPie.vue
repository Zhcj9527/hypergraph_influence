<template>
    <div class='detailed-pie' ref='root'>
    </div>
</template>

<script>
import * as d3 from 'd3'

export default {
    name: 'component_name',
    data() {
        return {}

    },
    props: [],
    methods: {
        draw(data) {

            // SVG画布边缘与图表内容的距离
            var margin = {top: 10, right: 30, bottom: 30, left: 60},
                width = 960 - margin.left - margin.right,
                height = 1080 - margin.top - margin.bottom
            var svg = d3.select('.detailed-pie').append('svg')
                .attr('width', width).attr('height', height)

                //  pie_chart data
            this.pie_data = data[0]["values"][0]["values"]
            console.log("pie_data", this.pie_data)
            this.category_num = this.pie_data[0].category_num
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
                .range([0, 35]);


            // var formatSum = d3.format(".1s");

            // var padding = 10;

            var color = d3.scaleOrdinal()
                .domain(this.category_num)
                .range(["#9400D3", "#FF1493", "#0000CD", "#00CED1", "#00BFFF"]);

            var arc = d3.arc()
                .padRadius(50);

            var pie = d3.pie()
                .sort(null)
                .padAngle(0.02)
                .value(function (d) {
                    return d.values;
                });

            var algorithm_svg = svg.append('g')
                .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
                .attr("class", "algorithm")
                .selectAll("g")
                .data(data)
                .enter().append("g")
                .attr("id", d => 'algorithm_group-'+ d.name)
                .attr("transform", function (d, i) {
                    return "translate(" + (i * 450)  + ",0)";
                });
                // .on("click", )  //添加事件，点击pie 会显示对应的层层之间的比较

            var period_svg = algorithm_svg.append("g")
                .attr("class", "period")
                .selectAll("g")
                .data(d => d.values)
                .enter().append("g")
                .attr("id", d => "period_group-" + d.period)
                .attr("transform", function (d, i) {
                    return "translate(0," + (i * 40)  + ")";
                });

            var pie_svg = period_svg.selectAll(".pie")
                .data(d => d.values)
                .enter().append("g")
                .attr("class", "pie")
                .attr("id", d => 'pie_group-'+ d.node )
                .each(multiple)
                .select("g");


            var label = pie_svg.append("text")
                .attr("class", "label")
                .attr("font-size", "10px")  // 设置文本大小

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
                    .attr("transform", "translate(" +  (2*r*i + 25) + "," + 35 + ")");

                svg.selectAll(".arc")
                    .data(function (d) {
                        return pie(d.category_list);
                    })
                    .enter().append("path")
                    .attr("class", "arc")
                    .attr("d", arc.outerRadius(r).innerRadius(r * 0.6))

                    .style("fill", function (d) {
                        return color(d.data.id);
                    })
                    .attr("stroke", "whitesmoke")
                    .attr("stroke-width", 0.5);
            }

        }

    },
    computed: {},
    watch: {},
    created() {

    },
    mounted() {

        var peroid_algorithm_list = []  // 定义一个存储点击PieChart视图的圆环对应的参数 {"period": d.period, "algorithm": d.algorithm}
        this.$bus.$on('algorithm-selected', (d) => {
            peroid_algorithm_list.push(d);
            console.log("click_pie_period_algoritnm", peroid_algorithm_list)

            this.$axios.post('get_nodes_data', peroid_algorithm_list)
            .then((res) => {
                var data = res.data
                console.log("detailed_pie_data", data);
                d3.select('.detailed-pie').selectAll('*').remove();  // 移除原来的画布所画内容
                this.draw(data);
            })
            .catch((error) => {
                console.log('get_nodes_data', error);
            })
        })
    }
}

</script>