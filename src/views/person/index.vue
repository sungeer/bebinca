<template>
<!--【核酸采集平台】 web/src/person template-->
  <div>
    <el-card :body-style="{'padding': '2px', 'text-align': 'center'}">
        <h1>预约信息查询</h1>
    </el-card>
    
    <el-card class="box">
      <div style="display:flex;padding-bottom:12px">
            <div style="margin-right:10px">
                <span style="width:50px;margin-right:10px">姓名</span>
                <el-input size="mini"  v-model="search.xm" style="width:100px"/>
            </div>
            <div style="margin-right:10px">
                <span style="width:50px;margin-right:10px">联系电话</span>
                <el-input size="mini"  v-model="search.lxdh" style="width:100px"/>
            </div>
            <div style="margin-right:10px">
                <span style="width:50px;margin-right:10px">居住地址</span>
                <el-input size="mini"  v-model="search.jzdz" style="width:100px"/>
            </div>
            <div>
                <el-button type="primary" size="mini" @click="doLoad">查询</el-button>
            </div>
        </div>
        <el-table
        :data="list"
        :height="height"
        border
        >
            <el-table-column label="编号" prop="id" />
            <el-table-column label="登记日期" prop="djrq" width="160px">
                <template slot-scope="scope">
                    {{ $moment(scope.row.djrq).format('YYYY年M月D日 HH:mm') }}
                </template>
            </el-table-column>
            <el-table-column label="姓名" prop="xm" />
            <el-table-column label="性别" prop="xb">
                <template slot-scope="scope">
                    {{ getXb(scope.row.xb) }}
                </template>
            </el-table-column>
            <el-table-column label="年龄" prop="nl" />
            <el-table-column label="出生日期" prop="csrq" width="120px">
                <template slot-scope="scope">
                    <span v-if="scope.row.csrq">{{ $moment(scope.row.csrq).format('YYYY年M月D日') }}</span>
                </template>
            </el-table-column>
            <el-table-column label="居住地址" prop="jzdz" />
            <el-table-column label="联系电话" prop="lxdh" />
            <el-table-column label="身份证号" prop="zjhm" />
        </el-table>
        <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page.sync="pager.page"
            :page-size="10"
            layout="total, prev, pager, next"
            :total="pager.count">
        </el-pagination>
    </el-card>
  </div>
</template>

<script>
/*【核酸采集平台】 web/src/person script */
import { getPersonList } from '@/api'
export default {
  name: 'Person',
  data() {
      return {
          height: window.innerHeight - 280, 
          list: [],   //预约数据列表，用于表格展示
          search: {   //查询条件
              xm: '',
              lxdh: '',
              jzdz: '',
          },
          pager: {    //分页参数
              count:0,
              page:1,
              size:10,
          }
      }
  },
  mounted() {        // 项目挂载方法，在进入页面后执行
      this.doLoad()  // 进入页面后，调用doLoad()方法
  },
  methods: {         //模板内的方法列表
      doLoad() {     //加载数据
          getPersonList(Object.assign(this.search, this.pager))
          .then(res=>{             //请求完成后的响应数据
              this.list = res.list // 响应数据中的list赋值给list
              this.pager.count = res.count  //响应数据中的总条件赋值给pager.count
          })
      },
      getXb(v) {     //根据性别编码获取性别名称的方法
          if (v == '1') {return '男'}
          else if (v == '2') {return '女'} 
          else {return '未知'}
      },            
      handleSizeChange(v) {    //改变分页数量时调用的方法
          this.pager.size = v;
          this.pager.page = 1;
          this.doLoad()
      },
      handleCurrentChange(v) {  //改变当前页面时调用的方法
          this.pager.page = v;
          this.doLoad()
      }
  }
}
</script>
<style scoped>
/*【核酸采集平台】 web/src/person style */
.box {
    margin-top:10px;
}
</style>