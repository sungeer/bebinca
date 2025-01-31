<template>
    <div>
        <el-card ref="code" :body-style="{'text-align': 'center'}">
            <div slot="header" class="clearfix" style="text-align:center">
            <span>核酸检测登记二维码</span>
            </div>
            <vue-qr :text="text" :size="360"/>
            <div style="width:100%;display:flex;justify-content: center;">
                <div style="font-size:24px; width: 400px">工作人员扫码使用，请勿外传</div>
            </div>
        </el-card>
        <!-- <div style="margin-top:10px;text-align:center">
            <el-button type="primary" size="large" @click="doPrint">打印</el-button>
        </div> -->
    </div>
</template>
<script>
import vueQr from 'vue-qr'
export default {
     components: {vueQr},
    data() {
        return {
            text: window.location.host + '/h5/index.html#/checkin',
        }
    },
    methods: {
        // doPrint() {
        //     //保存原来的页面内容
        //     var oldHtml = window.document.body.innerHTML;
        //     //将页面内容修改为要打印的HTML标签
        //     window.document.body.innerHTML = this.$refs.code.$el.innerHTML;
        //     //调出打印对话框
        //     print()
        //     //打印完成后，恢复页面内容
        //     window.document.body.innerHTML = oldHtml
        // }
    }
}
</script>