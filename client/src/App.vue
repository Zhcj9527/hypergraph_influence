<template>
    <div id="app">
<!--        <header class="navbar navbar-dark sticky-top bg-dark flex-md-nowrap p-0 shadow">-->
<!--            <a class="navbar-brand col-md-3 col-lg-2 me-0 px-3" href="#">Hypergraph Influence Vis</a>-->
<!--        </header>-->
        <div id="left-panel">
            <div class="panel-container">
                <div id="left-top" class="bl-card-shadow">
                    <div class="view-title">&ensp;</div>
                    <div class="view" id="contral" >
                        <div id="left-top-content">
                            <div class="view-content">
                                <div class="dropdown" style="width: 280px">
                                    <label for="datasets" style="width: 80px">Datasets: </label>
                                    <select name="networks" id="datasets" @change="getDataset($event.target.value)"
                                            class="selectpicker show-tick form-control" data-live-search="true" data-width="200px">
                                        <option v-for="network in networks" :key="network"> {{network}} </option>
                                    </select>
                                </div>
                                <div class="sources">
                                    <label for="T">Number of Stages of Propagation(T): </label>
                                    <form name="myForm" id="T-num" @change="getTnum($event.target.value)">
                                        <input type="radio" name="time" value="15"> 15&ensp;
                                        <input type="radio" name="time" value="25" checked="true"> 25&ensp;
                                        <input type="radio" name="time" value="35"> 35
                                    </form>
                                </div>
                                <div class="sources">
                                    <label for="sources">Number of Source Nodes(K): </label>
                                    <form name="myForm" id="sources-num" @change="getSource($event.target.value)">
                                        <input type="radio" name="coverage" value="5"> 5&ensp;
                                        <input type="radio" name="coverage" value="10"> 10&ensp;
                                        <input type="radio" name="coverage" value="15"> 15&ensp;
                                        <input type="radio" name="coverage" value="20"> 20&ensp;
                                        <input type="radio" name="coverage" value="25" checked="true"> 25
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div id="left-bottom">
                    <div class="view-title">&ensp;
                        <div id="alg" @change="getAlg($event.target.value)" style="position: relative; float: right; right: 10%; top: 0px; height: 20px; opacity: 0.5">
                            <p>#Model: <input id="selected_alg" style="height: 20px; width: 60px;text-align:center" type="text" name="vg" value="" /></p>
                        </div>
                    </div>
                    <hot-chart id="hotmap" class="view"></hot-chart>
                </div>
            </div>
        </div>
        <div id="right-panel">
            <div class="panel-container">
                <div id="right-top">
                    <div class="view-title">
                        <div class="switch">
                            <label for="label">#outlineArc:</label>
                            <input type="checkbox" class="switch-button" id="switch-button"
                                   checked="true" @change="getSwitch($event.target.checked)">
                            <label for="switch-button"> OFF </label>
                        </div>
                    </div>
                    <div class="view" id="right-top-content">
                        <div id="right-top-left">
                            <div class="view-content">
                                <div class="dropdown">
                                    <label for="algorithm">Cascade Model A:</label>
                                    <select name="btn" id="left-btn" @change="selectValue($event.target.value)"
                                            class="selectpicker show-tick form-control" data-live-search="true" data-width="100px">
                                        <option v-for="algorithm in algorithms" :key="algorithm"> {{algorithm}} </option>
                                    </select>
                                </div>
                                <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
                                  <line x1="0" y1="0" x2="100" y2="0" style="stroke: #e5e5e7;stroke-width:4" />
                                </svg>
                            </div>
                            <div><pattern-comparator></pattern-comparator></div>
                        </div>
                        <div id="right-top-mid">
                            <div class="view-content">
                                <div id="left-frequency">
                                    <input id="left-text" type="text" name="frequency" value="" />
                                </div>
                                <div id="mid-frequency">
                                    <input id="mid-text" type="text" name="frequency" value="" />
                                </div>
                                <div id="right-frequency">
                                    <input id="right-text" type="text" name="frequency" value="" />
                                </div>
                                <svg style="height: 34px; width: 265px;" id="mid-line"  xmlns="http://www.w3.org/2000/svg" version="1.1">
                                    <line x1="30" y1="15" x2="128" y2="15" style="stroke: #e5e5e7; stroke-width:2" />
                                    <line x1="30" y1="0" x2="30" y2="30" style="stroke: #e5e5e7;stroke-width:2" />
                                    <line x1="128" y1="0" x2="128" y2="30" style="stroke: #e5e5e7;stroke-width:2" />
                                </svg>
                                <div id="slider">
                                     <input type="text" class="js-range-slider" name="my_range" value="" />
                                </div>
                            </div>
                            <horizon-bar></horizon-bar>
                        </div>
                        <div id="right-top-right">
                            <div class="view-content">
                                <div class="dropdown">
                                <label for="algorithm">Cascade Model B:</label>
                                <select name="btn" id="right-btn" @change="selectValue2($event.target.value)"
                                        class="selectpicker show-tick form-control" data-live-search="true" data-width="100px">
                                    <option v-for="algorithm in algorithms" :key="algorithm"> {{algorithm}} </option>
                                </select>
                                </div>
                                <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
                                  <line x1="0" y1="0" x2="100" y2="0" style="stroke: #e5e5e7;stroke-width:4" />
                                </svg>
                            </div>
                            <div><pattern-comparator2></pattern-comparator2></div>
                        </div>
                    </div>
                </div>
                <div id="right-top2">
                    <div class="view-title">&ensp;</div>
<!--                    <force-direct class="view"></force-direct>-->
                    <BoxChart class="view"></BoxChart>
                </div>
                <div id="right-bottom-left">
                    <div class="view-title">&ensp;

                        <div id="vg" @change="getId($event.target.value)" style="position: relative; float: right; right: 60%; top: 0px; height: 20px; opacity: 0.5">
                            #ID: <input id="selected_vg" style="height: 20px; width: 60px;text-align:center" type="text" name="vg" value="" />
                        </div>
                        <div id="vg1" @change="getId1($event.target.value)" style="position: relative; float: right; right: 23%; top: 0px; height: 20px; opacity: 0.5">
                            #CUM: <input id="selected_vg1" style="height: 20px; width: 72px;text-align:center" type="text" name="vg" value="" />
                        </div>
                        <div id="vg2" @change="getId2($event.target.value)" style="position: relative; float: right; right: -15%; top: 0px; height: 20px; opacity: 0.5">
                            #IND: <input id="selected_vg2" style="height: 20px; width: 82px;text-align:center" type="text" name="vg" value="" />
                        </div>


<!--                        <form name="myForm" @change="getRadio($event.target.value)" style="position: center; width: 100px; height: 26.39px; float: right;-->
<!--                        /*top:30px;*/-->
<!--                        /*left:460px;*/-->
<!--                        line-height:20.5px;">-->
<!--                            <input type="radio" name="coverage" value="Individual coverage">Ind-->
<!--                            <input type="radio" name="coverage" value="Cumulative coverage" checked="true">Cum-->
<!--                        </form>-->
                    </div>
                    <cov-ratio class="view"></cov-ratio>
                </div>
                <div id="right-bottom-right">
<!--                    <div class="view-title">&ensp;Parallel Coordinate View-->
<!--                        <div id="vg" @change="getId($event.target.value)" style="position: relative; float: right; right: 65%; top: 2px; height: 26.39px;">-->
<!--                            <p>Id: <input id="selected_vg" style="height: 20px; width: 60px;text-align:center" type="text" name="vg" value="" /></p>-->
<!--                        </div>-->
<!--                        <div id="icon1" style="position: relative; float: right; right: 52.5%;">-->
<!--                            <button type="button" class="btn btn-outline-secondary">-->
<!--                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-activity" viewBox="0 0 16 16">-->
<!--                                    <path fill-rule="evenodd" d="M6 2a.5.5 0 0 1 .47.33L10 12.036l1.53-4.208A.5.5 0 0 1 12 7.5h3.5a.5.5 0 0 1 0 1h-3.15l-1.88 5.17a.5.5 0 0 1-.94 0L6 3.964 4.47 8.171A.5.5 0 0 1 4 8.5H.5a.5.5 0 0 1 0-1h3.15l1.88-5.17A.5.5 0 0 1 6 2Z"/>-->
<!--                                </svg>-->
<!--                            </button>-->
<!--                        </div>-->
<!--                    </div>-->
                    <par-coords></par-coords>
                    <div class="view-title">&ensp; </div>
                    <force-direct class="view"></force-direct>
<!--                    <scatter-chart class="view"></scatter-chart>-->
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import $ from 'jquery'
// import LineChart from "./components/LineChart";
// import HgraphBipartite from "./components/HgraphBipartite";

// import PieChart from "./components/PieChart";
// import DetailedPie from "./components/DetailedPie";
// import AlgLines from "./components/AlgLines";
// import BarChart from "./components/BarChart";

import HotChart from "./components/HotChart";
import ParCoords from "./components/ParCoords";
// import ScatterChart from "./components/ScatterChart";
import BoxChart from "./components/BoxChart"
import CovRatio from "./components/CovRatio";
import PatternComparator from "./components/PatternComparator";
import PatternComparator2 from "./components/PatternComparator2"
import HorizonBar from "./components/HorizonBar";
import ForceDirect from "./components/ForceDirect";


export default {
  name: 'App',
  components: {
      ForceDirect,
      HorizonBar,
      PatternComparator2,
      PatternComparator,
      CovRatio,
      // ScatterChart,
      BoxChart,
      ParCoords,
      HotChart,
    // LineChart,
    // HgraphBipartite,
    //   ForceDirect,

      // PieChart,
      // DetailedPie,
      // AlgLines,
      // BarChart,


  },
    data(){
        return{

            algorithms : ["agr_1" , "agr_2", "agr_3", "agr_4", "agr_5", "agr_6", "agr_7", "agr_8"],
            // algorithms : [{"agr_1": HDD}, ],
            networks : ["Algebra", "Bars-Rev", "Music", "Restaurants-Rev", "chuancai", "yuecai", "Music-Rev"]

        }

    },
    props:[],
    methods:{

        getDataset(val) {
            console.log(val)
            this.$bus.$emit('dataset-selected-control panel', {"dataset": val})
        },

        getSource(val) {
            console.log(val)
        },

        // vue中使用@change获取select下拉框选中的值
        selectValue(val) {
            console.log(val)
            this.$bus.$emit('algorithm-selected-pat1', {"algorithm": val})},

        selectValue2(val) {
            console.log(val)
            this.$bus.$emit('algorithm-selected-pat2', {"algorithm": val})},

        getSwitch(val){
           console.log(val);
           this.$bus.$emit('switch-selected-pat', {"value": val})
        },

        getId(val) {
            console.log(val)
            this.$bus.$emit('vgId-selected-par', {"id": val})
        },



    },
    computed:{

    },
    watch:{

    },
    created(){

    },
    mounted(){
        this.$bus.$on("left-rect-mouseover", d =>{
            document.getElementById("left-text").value = d
        })
        this.$bus.$on("left-rect-mouseout", d => {
            // 鼠标移开之后 left-text显示总频率
            document.getElementById("left-text").value = d
        })

        $(".js-range-slider").ionRangeSlider({
            type: "double",
            skin: "big",
            step: 5,
            min: 0,
            max: 100,
            grid: false,
            from: 15,      // set min position for FROM handle (replace FROM to TO to change handle)
            to: 85,
            hide_min_max: true,    // show/hide MIN and MAX labels
            hide_from_to: true,    // show/hide FROM and TO labels

            onChange: function (data) {
                var to_pretty = parseInt(data.to_pretty),
                    from_pretty = parseInt(data.from_pretty);

                var val = parseFloat(to_pretty-from_pretty) + "%"
                document.getElementById("mid-text").value = val
                // console.log(data)
            }
        });

        this.$bus.$on("right-rect-mouseover", d =>{
            document.getElementById("right-text").value = d
        })
        this.$bus.$on("right-rect-mouseout", d => {
            // 鼠标移开之后 left-text显示总频率
            document.getElementById("right-text").value = d
        })

        this.$bus.$on("alg-mouseover", d =>{
            document.getElementById("selected_alg").value = d
        })



        this.$bus.$on("selected_vg-mouseover", d =>{
            console.log(d)
            document.getElementById("selected_vg").value = d
            document.getElementById("selected_vg").style.color = "steelblue"
            document.getElementById("selected_vg").style.caretColor = "red"
            this.$bus.$emit("highlighted_vg-mouseover", d)

            this.$bus.$on("selected_vg-mouseout", d => {
            this.$bus.$emit("highlighted_vg-mouseout", d)
            })
        })

        this.$bus.$on("selected_cum-mouseover", d =>{
            console.log(d)
            document.getElementById("selected_vg1").value = d
            document.getElementById("selected_vg1").style.color = "steelblue"
            document.getElementById("selected_vg1").style.caretColor = "red"
        })

        this.$bus.$on("selected_ind-mouseover", d =>{
            document.getElementById("selected_vg2").value = d
            document.getElementById("selected_vg2").style.color = "steelblue"
            document.getElementById("selected_vg2").style.caretColor = "red"
        })









    },
}
</script>

<style>
/*#app {*/
/*    font-family: 'Avenir', Helvetica, Arial, sans-serif;*/
/*    -webkit-font-smoothing: antialiased;*/
/*    -moz-osx-font-smoothing: grayscale;*/
/*    color: #2c3e50;*/
/*    !*display: flex;*!*/
/*    height: 100%;}*/
#app {
      /*position: absolute;*/
      /*width: 100%;*/
      /*height: 100%;*/
      /*!* background-color: #e9f1ed; *!*/
      font-family: 'Avenir', Helvetica, Arial, sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      color: #2c3e50;
      display: flex;
      height: 100%;
    }
    #left-panel {
      position: absolute;
      top: 10px;
      bottom: 10px;
      left: 10px;
      right: calc(70% + 10px);
      display: flex;
      flex-direction: column;
    }

    #right-panel {
      position: absolute;
      top: 10px;
      bottom: 10px;
      right: 10px;
      left: calc(30% - 10px);
      display: flex;
      flex-direction: column;
    }
    .panel-container {
      position: relative;
      flex: auto;
      /*border-radius: 15px;*/
      /*border: 2px solid rgb(96, 96, 96);*/
    }
    #left-top {
      position: absolute;
      top: 0;
      bottom: 81%;
      left: 0px;
      right: 0px;
      display: flex;
      flex-direction: column;
    }
    #left-top-content {
      position: absolute;
      top: 20px;
      bottom: 10px;
      left: 10px;
      right: 0px;
      display: flex;
      flex-direction: column;
    }
    .sources {
        position: relative;
        top: 5px;
    }
     #T-num {
         position: absolute;
        width: 150px;
        float: right;
        top: 2px;
        right: 17%;
     }
    #sources-num {
        position: absolute;
        width: 250px;
        float: right;
        top: 2px;
        right: 10%;
    }
    #left-bottom {
      position: absolute;
      top: 20%;
      bottom: 0;
      left: 0px;
      right: 0px;
      display: flex;
      flex-direction: column;
    }
    #right-top {
      position: absolute;
      top: 0;
      bottom: 41%;
      /*  top: 20%;*/
      /*  bottom: 0;*/
      left: 10px;
      right: calc(40%);
      display: flex;
      flex-direction: column;
    }
    #right-top2 {
      position: absolute;
      top: 0;
      bottom: 41%;
      left: calc(60% + 10px);
      right: 0;
      display: flex;
      flex-direction: column;
    }
    #right-top-left {
      position: absolute;
      top: 10px;
      bottom: 10px;
      left: 10px;
      /*right: calc(60% + 10px);*/
        right: calc(60%);
      display: flex;
      flex-direction: column;
    }
    #right-top-right {
      position: absolute;
      top: 10px;
      bottom: 10px;
      /*left: calc(60% + 10px);*/
        left: calc(60%);
      right: 10px;
      display: flex;
      flex-direction: column;
    }
    #right-top-mid {
      position: absolute;
      top: 10px;
      bottom: 10px;
      left: 40%;
      right: 40%;
      display: flex;
      flex-direction: column;
    }
    #left-frequency {
        position: relative;
        float: left;
        height: 26.39px;
        bottom: 10px;
        left: 10px;
    }
    #mid-frequency {
        position: relative;
        float: right;
        height: 26.39px;
        bottom: 4px;
        right: 59px;
    }
    #right-frequency {
        position: relative;
        float: right;
        height: 26.39px;
        bottom: 10px;
        right: 10px;
        left: 30px;
    }
    #left-text,#right-text {
        height: 20px;
        width: 40px;
        border-style:none none solid none;
        border-width: thin;
        border-color: #f7f7f7;
        border-radius: 10px;
        background-color: #ececec;
        text-align:center;
    }
    #mid-text {
        height: 20px;
        width: 40px;
        border-style:none none solid none;
        text-align:center;
    }
    #mid-line {
        position: relative;
        bottom: 14px;
    }
    /* 滑块css */
    #slider {
        position: relative;
        width: 98px;
        left: 30px;
        bottom: 68px;
    }
    #right-bottom-left {
      position: absolute;
      top: 60%;
      bottom: 0px;
      left: 10px;
      right: calc(40%);
      display: flex;
      flex-direction: column;
    }
    #right-bottom-right {
      position: absolute;
      top: 60%;
      bottom: 0px;
      left: calc(60% + 10px);
      right: 0px;
      display: flex;
      flex-direction: column;
    }
    .view {
      position: relative;
      flex: auto;
      display: flex;
      border: 1.5px solid rgb(247, 247, 247);
    }
    .view-title {
      font-size: 1.1rem;
      /*font-weight: bold;*/
      text-align: left;
      flex-direction: column;
      background: rgb(253, 252, 252);
      /*border-radius: 3px;*/
      height: 26.39px;
    }
    .view-content {
      font-size: 1.1rem;
      text-align: left;
      flex-direction: column;
      background: #ffffff;
      height: 26.39px;
    }

    /* 下拉列表的css */
    .dropdown.bootstrap-select.show-tick.form-control {
        float: right;
        bottom: 7px;
        right: 2px;
        height: 26.39px;
    }
    .btn.dropdown-toggle.btn-light {
        /*height: 26.39px;*/
        border-width: 0.2px;
        border-color: #fcf9f9;
        background-color: #fff;
    }

    /* 利用css的伪元素生成一个按钮，根据表单checkbox的checked属性来控制开关的状态和样式的切换。 */
    .switch {
        position: relative;
        float: right;
        right: 10%;
    }
    .switch-button{
        display: none;/*隐藏表单元素*/
    }
    .switch-button+label{/*+选择器选择紧跟“+”左边选择器的第一个元素*/
        display: inline-block;
        position: relative;
        transition: all .3s;
        width: 60px;
        height: 26.38px;
        border: 1px solid #999;
        border-radius: 15px;
        background-color: #ccc;
    }
    .switch-button:checked+label{/*选中表单后的样式，:checked表示checkbox被选中后的状态*/
        background-color: lightgreen;
    }
    .switch-button+label::before{/*使用伪元素生成一个按钮*/
        content: '';
        display: block;
        height: 24px;
        width: 25px;
        position: absolute;
        border-radius: 25px;
        left: 2px;
        top: 0px;
        bottom: 1px;
        background-color: #fff;
        box-shadow: 0 1px 3px rgba(0, 0, 0, .4);
        transition: all .3s;
    }
    .switch-button:checked+label::before{/*checkbox选中时按钮的样式*/
        left: 32px;
        transition:  all .2s linear;
    }
    /* icon1 */
    .btn.btn-outline-secondary {
        position: relative;
        width: 22px;
        height: 22px;
        bottom: 2px;
    }
    .bi.bi-activity {
        position: relative;
        right: 7px;
        bottom: 8px;
    }
</style>
