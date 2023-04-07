<template>
    <div class='force-direct' ref='root'>
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
    methods: {
        draw(data) {
            //  seeds是源节点
            this.seeds = uniq(data.seeds_data.seeds_list)
            this.seeds_he = uniq(data.seeds_data.seeds_he)
            this.he_vlist = uniq(data.seeds_data.seeds_he_list)

            console.log("seeds", this.seeds)
            console.log("seeds_he", this.seeds_he)
            console.log("he_vlist", this.he_vlist)


            // 是传播路径的第一阶段 seed_num_info["activated_seeds_bytime"][0] 的传播节点
            this.P1 = ['11', '28']
            this.P2 = ['12','21','37']



            this.hyper_data = data.hyper_data
            this.nodes = data.hyper_data.nodes;
            this.links = data.hyper_data.links;
            this.labels = data.labels;

            console.log("hyper_data", this.hyper_data)
            console.log('nodes', this.nodes);
            console.log('links', this.links);
            console.log("labels", this.labels)

            this.$bus.$emit("vg-labels", this.labels)

            // 给超边加上标签
            let label = assign_hyperedge_labels(this.hyper_data, this.labels);
            console.log(label)

            function assign_hyperedge_labels(hyper_data, label_map) {
                hyper_data.nodes.forEach(node=>{
                    let label = "";
                    let n_list = node.id.split("|");
                    n_list.forEach(n=>{
                        if(label_map[n]){
                            label += label_map[n] + "|";
                        }
                    })
                    label = label.substring(0, label.length - 1);
                    node.label = label;
                })
            }


            // var width = 527;
            // var height = 508;
            var width = 527;
            var height = 330;
            var svg = d3.select('.force-direct')
                .append("svg")
                .attr("width", width)
                .attr("height", height)
                .call(d3.zoom() //创建缩放行为
                    .scaleExtent([-5, 10])
                    .on('zoom', zoom_actions)); //设置缩放范围

            //初始化力学仿真器，通过布局函数格式化数据
            var simulation = d3.forceSimulation()
                .force("link", d3.forceLink().id(function(d) { return d.id; })) //distance设置连线距离.
                .force("charge", d3.forceManyBody())  //注1>
                .force("center", d3.forceCenter(width / 2, height / 2));  //设置力学仿真器的中心

            simulation
                .nodes(this.nodes)
                .on("tick", ticked);

            simulation
                .force("link")
                .links(this.links);

            // //添加group包裹svg元素以进行缩放，目的是在缩放时不会影响整个容器的位置
            this.svg_g = svg.append("g")
                .attr("class", "everything");

            // 定义links、nodes、vertices的group
            this.links_group = this.svg_g.append("g")
                .attr("id", "hyper_links_group");
            this.nodes_group = this.svg_g.append("g")
                .attr("id", "hyper_nodes_group");
            this.vertices_group = this.svg_g.append("g")
                .attr("id", "hyper_vertices_group");


            // ======================= links ======================

            let lg = this.links_group.selectAll("line").data(this.links);
            lg.exit().remove();
            lg = lg.enter().append("line").merge(lg)
                // .attr("stroke-width", 0.5)
                // .style("stroke", "#ccc")
                .attr("id", d => "hgraph-edge-"+ d.source.id.replace(/[|]/g,"")+"-"+ d.target.id.replace(/[|]/g,""))
                .attr("class", "hyper_edge")
                .style("visibility", (d) => {
                    for ( let i=0; i<this.seeds.length; i++) {
                        if ( this.seeds_he.includes(d.source.id) ) {
                            return "visible"
                        }
                        for (let j=0; j<this.seeds_he.length; j++) {
                           if (this.seeds_he.includes(d.source.id) && this.seeds.includes(d.target.id) ) {
                               return "visible"
                            } else {
                                return "hidden"
                            }
                        }
                    }
                })

            //  ================== nodes/text ========================
            var hg = this.nodes_group.selectAll("g").data(this.nodes.filter(d => d.bipartite===1));
            hg.exit().remove();
            hg = hg.enter().append("g").merge(hg)
                .attr("id", d=>'hg-nodegroup-'+ d.id.replace(/[|]/g,""))
                .attr("class", "he-group")
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended)
                );

            hg.append("circle")
                .attr("r", 15)
                // .attr("fill", "#7be0bf") // origin
                .attr("fill", "rgb(33, 133, 208)")
                .attr("id", d => 'hg-node-'+ d.id.replace(/[|]/g,""))
                .attr("class", "hyper_node")
                .style("visibility", (d) => {
                    if (this.seeds_he.includes(d.id) ) {
                        return "visible"
                    } else {
                        return "hidden"
                    }
                });

            hg.append("text")
                .attr("dx", 5)
                .attr("dy", 2)
                .attr("class", "node-label")
                .attr("id", d => 'hg-text-'+ d.id.replace(/[|]/g,""))
                .text(d => d.label)
                // .style("visibility", (d) => {
                //     if (this.seeds_he.includes(d.id)) {
                //         return "visible"
                //     } else {
                //         return "hidden"
                //     }
                // });
                .style("visibility", "hidden");

            var vg = this.vertices_group.selectAll("g").data(this.nodes.filter(d => d.bipartite===0));
            vg.exit().remove();
            vg = vg.enter().append("g").merge(vg)
                .attr("id", d=>'vg-nodegroup-'+ d.id.replace(/[|]/g,""))
                .attr("class", "v-group")
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended)
                );

            vg.append("circle")
                // .attr("r", 5)
                .attr("r", d => {
                    if ( this.seeds.includes(d.id )) {
                        return 15
                    } else if ( this.he_vlist.includes(d.id) ) {
                        return 15
                    }
                })
                // .attr("fill", "#FF0000")
                .attr("fill", d => {
                    if ( this.seeds.includes(d.id )) {
                        // return "#ec8b8b" // origin
                        return 'rgb(219, 40, 40)'
                    } else if ( this.he_vlist.includes(d.id) ) {
                        return "#ccc"
                    }
                })
                .attr("id", d => 'vg-node-'+ d.id.replace(/[|]/g,""))
                .attr("class", "vertex_node")
                .style("visibility", (d) => {
                    if (this.seeds.includes(d.id) || this.he_vlist.includes(d.id) ) {
                        return "visible"
                    } else {
                        return "hidden"
                    }
                });

            vg.append("text")
                .attr("dx", 5)
                .attr("dy", 2)
                .attr("class", "node-label")
                .attr("id", d => 'vg-text-'+ d.id.replace(/[|]/g,""))
                .text(d => d.label)
                .style('visibility', 'hidden')
                // .style("visibility", (d) => {
                //     if (this.seeds.includes(d.id)) {
                //         return "visible"
                //     } else {
                //         return "hidden"
                //     }
                // })
                .on('mouseover', function() {
                    d3.select(this).style("visibility", "visible");
                })
                .on('mouseout', function() {
                    d3.select(this).style("visibility", "hidden");
                });

            //监听拖拽开始
            function dragstarted(d) {
                if (!d3.event.active) simulation.alphaTarget(0.3).restart(); //alpha是动画的冷却系数，运动过程中会不断减小，直到小于0.005为止，此时动画会停止。
                d.fx = d.x;    //fx为固定坐标，x为初始坐标  注3>
                d.fy = d.y;
            }

            //监听拖拽中
            function dragged(d) {
                d.fx = d3.event.x;  //fevent.x为拖拽移动时的坐标
                d.fy = d3.event.y;
            }

            //监听拖拽结束
            function dragended(d) {
                if (!d3.event.active) simulation.alphaTarget(0);
                d.fx = null;        //固定坐标清空
                d.fy = null;
            }

            let that = this
            function zoom_actions() {
                that.svg_g.attr("transform", d3.event.transform)
            }

            //拖拽时的事件监听器  以实时更新坐标
            function ticked() {
                lg
                    .attr("x1", function (d) { return d.source.x; })
                    .attr("y1", function (d) { return d.source.y; })
                    .attr("x2", function (d) { return d.target.x; })
                    .attr("y2", function (d) { return d.target.y; });

                hg.selectAll(".hyper_node")
                    .attr("cx", function (d) { return d.x; })
                    .attr("cy", function (d) { return d.y; });
                hg.selectAll(".node-label")
                    .attr("x", function (d) { return d.x; })
                    .attr("y", function (d) { return d.y; });

                vg.selectAll(".vertex_node")
                    .attr("cx", function (d) { return d.x; })
                    .attr("cy", function (d) { return d.y; });
                vg.selectAll(".node-label")
                    .attr("x", function (d) { return d.x; })
                    .attr("y", function (d) { return d.y; });
            }

            // js数组去重
            function uniq(array){
                let temp = []; //一个新的临时数组
                for(let i = 0; i < array.length; i++){
                    if(temp.indexOf(array[i]) === -1){
                        temp.push(array[i]);
                    }
                }
                return temp;
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
        // this.draw()

        // this.$axios.get('get_hgraph_data')
        //     .then((res) =>{
        //         var data = res.data
        //         console.log("data", data)
        //         this.draw(data)
        //         // this.constructor(data)
        //
        //         // this.draw_hypergraph()
        //     })
        //     .catch((error) =>{
        //         console.log('get_hgraph_data', error)
        //     })



        this.$bus.$on('final-nodes', (d) => {
            console.log(d)
            this.$axios.post('get_hgraph_data', d)
            .then((res) => {
                d3.select('.force-direct').selectAll('*').remove();  // 移除原来的画布所画内容
                var data = res.data
                console.log("str_data", data);
                this.draw(data)
            })
            .catch((error) => {
                console.log('get_hgraph_data', error);
            })
        })

        // this.$bus.$on("selected_vg-mouseover", d =>{
        //     console.log(d)
        // })

        this.$bus.$on("vg-labels", labels =>{
            console.log(labels)
            var periodList = []
            this.$bus.$on("selected_period_included_vg", period_vg => {

                console.log(period_vg)

                period_vg.forEach( d => {
                    console.log(d.node)
                    for (let vg in labels) {
                        if (labels[vg]===d.node) {
                            periodList.push(vg)
                        }
                    }
                })
                d3.selectAll(".vertex_node").attr("r", 5)
                                        .attr("fill", "#ccc")
                d3.selectAll(".node-label").style("visibility", "hidden")

                periodList.forEach( d => {
                    d3.select("#vg-node-" + d).attr("r", 10)
                                        .attr("fill", "#e33f3f")
                    d3.select("#vg-text-" + d).style("visibility", "visible")
                })
            })
            console.log(periodList)

            //
            //     if (periodList !== period_vg) {
            //         period_vg.forEach( d => {
            //             d3.select("#vg-" + d.node).style("visibility", "visible")
            //         })
            //         console.log(period_vg)
            //         periodList.forEach( d => {
            //             d3.select("#vg-" + d.node).style("visibility", "hidden")
            //         })
            //         console.log(periodList)
            //     }
            //     periodList = period_vg
        })



        // this.$bus.$on("hyper_data_process", (data) =>{
        //     this.nodes = hyper_data.nodes
        //     this.links = hyper_data.links
        //
        //     this.draw(data)  // 传数据的时候 组件间传值，两个组件要同时运行，emit/on 传过来的数据才可以用  或者定义一个全局的变量 在on所在函数里面
                            //传过来的数据赋值给那个全局变量 然后就可以在on 所在函数里面调用了 传输过来的数据就可以用了

            // console.log(this.nodes)
        // })

        // console.log(this.nodes)
    }
}
</script>