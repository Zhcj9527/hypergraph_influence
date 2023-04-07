<template>
    <div class='pie-chart' ref='root'>
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
                width = 600 - margin.left - margin.right,
                height = 1080 - margin.top - margin.bottom
            var svg = d3.select('.pie-chart').append('svg')
                .attr('width', width + margin.left + margin.right).attr('height', height + margin.top + margin.bottom)
                .attr('transform', 'translate(' + margin.right + ',' + margin.top + ')')
                // .attr("preserveAspectRatio", "xMidYMid meet")  // 自适应窗口
                // .attr("viewBox", "10 60" +' ' + width + ' ' + height )  //从左到右依次为：x坐标点起始位置，y坐标点起始位置，视图宽度，视图高度
                // .append('g')
                // .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
                // .attr("float", "left")
                // .call(d3.zoom() //创建缩放行为
                //     .scaleExtent([-2, 5])
                //     .on('zoom', zoomed)); //设置缩放范围

            // var data = [{
            //     state: "source",
            //     sum: 7659,
            //     ages: [{"age": 0, "population": 1735}, {"age": 1, "population": 2146}, {"age": 2, "population": 2976},
            //         {"age": 3, "population": 444}, {"age": 4, "population": 358}]
            // }
            // ]

                //  pie_chart data
            this.pie_data = data.pie_dict[1]["values"]
            console.log("pie_data", this.pie_data)
            this.category_num = this.pie_data[0].category_num
            console.log("category_num",this.category_num)
            this.vlabel2id = data.vlabel2id
            console.log("vlabel2id",this.vlabel2id)
            this.links = data.hyper_data.links
            console.log("links", this.links)
            this.categoryId = this.pie_data[0].category
            console.log("categoryId", this.categoryId)


                // 原来可以按照 sum 总和衡量大小的
            var radius = d3.scaleSqrt()
                // .domain([0, d3.max(data.pie_dict, function (d) {return parseInt(d.sum);})])
                .domain([
                    0,
                    d3.max(data.pie_dict, function(c) { return d3.max(c.values, function(d) { return parseInt(d.sum); }); })
                ])
                .range([0, 35]);

            //      // 自己按照
            // var radius = d3.scaleSqrt()
            //     .domain([0, 226])
            //     .range([0, 35]);


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

            var legend = svg
                .append('g')
                .attr("class", "legend")
                .selectAll("g")
                .data(this.category_num)
                .enter().append("g")
                .attr("id", d => 'legend_group-'+ d )
                .attr("transform", function (d, i) {
                    return "translate(-5," + (i * 20) + ")";
                });

            legend.append("rect")
                .attr("width", 18)
                .attr("height", 18)
                .style("fill", color);

            legend.append("text")
                .attr("x", 24)
                .attr("y", 9)
                .attr("dy", ".35em")
                .text(function (d) {
                    return d;
                });

            var algorithm_svg = svg.append('g')
                .attr("class", "algorithm")
                .selectAll("g")
                .data(data.pie_dict)
                .enter().append("g")
                .attr("id", d => 'algorithm_group-'+ d.name )
                .attr("transform", function (d, i) {
                    return "translate(" + (i * 70)  + ",0)";
                })
                .on("click",  (d) => {
                    this.$bus.$emit('algorithm-selected',
                        {"algorithm": d.name})
                });  //添加事件，点击pie 会显示对应的层层之间的比较



            var pie_svg = algorithm_svg.selectAll(".pie")
                .data(d => d.values)
                .enter().append("g")
                .attr("class", "pie")
                .attr("id", d => 'pie_group-'+ d.period )
                .each(multiple)
                .select("g")
                // .on("click",  (d) => {
                //     this.$bus.$emit('period-algorithm-selected',
                //         {"period": d.period, "algorithm": d.algorithm})
                // });  //添加事件，点击pie 会显示对应的层层之间的比较


            var label = pie_svg.append("text")
                .attr("class", "label")
                .attr("font-size", "10px")  // 设置文本大小

            label.append("tspan")
                .attr("class", "label-name")
                .attr("x", "-1.1em")
                .attr("dy", "-.2em")
                .text( d => d.period );

            label.append("tspan")
                .attr("class", "label-value")
                .attr("x", "-1.1em")
                .attr("dy", "1.1em")
                .text( d => d.sum );



            function multiple(d, i) {
                var r = radius(parseInt(d.sum));
                // var r = radius(75);

                var svg = d3.select(this)
                    .append("g")
                    .attr("transform", d => {
                        let r = radius(parseInt(d.sum));
                        if (r > 20) {
                            return "translate(" +  70 + "," + (60*i + 25) + ")";
                        }
                        else return "translate(" +  70 + "," + (60*i + 25) + ")";
                    })



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


                // // 获取传播节点对应的标签
                // function getSeedslist(d) {
                //     let seeds_list = []
                //     d.vg_list.forEach( v => {
                //         if (Object.keys(that.vlabel2id).includes(v)) {
                //             seeds_list.push(that.vlabel2id[v]);
                //         }
                //     })
                //     return seeds_list;
                // }
                //
                // // 获取传播节点对应的超边
                // function getSeedshe(seeds_list) {
                //     let seeds_he = []
                //     that.links.forEach( v => {
                //         if (seeds_list.includes(v.target)) {
                //             seeds_he.push(v.source);
                //         }
                //     })
                //     return seeds_he;
                // }
                //
                // // 判断此超边属于那一类 id, 超边可能会有多个，所以返回的是一个 id_list
                // function getId(seeds_he) {
                //     let id_list = []
                //     that.categoryId.forEach( v => {
                //         seeds_he.forEach( he => {
                //             if ( v.values.includes(he) ) {
                //                 id_list.push(v.id);
                //             }
                //         })
                //     })
                //
                //     return id_list
                // }



            }

            // function zoomed() {
            //     svg.attr("transform", d3.event.transform);
            // }
        }

    },
    computed: {},
    watch: {},
    created() {

    },
    mounted() {
        this.$axios.get('get_pie_data')
            .then((res) =>{
                var data = res.data
                console.log("data", data)
                this.draw(data)
            })
            .catch((error) =>{
                console.log('get_pie_data', error)
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