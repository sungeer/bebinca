<template>
  <div>
    <el-card :body-style="{'padding': '2px', 'text-align': 'center'}">
        <h1>登记信息查询</h1>
    </el-card>
    <el-card class="box">
        <div style="display:flex;padding-bottom:12px">
            <div style="margin-right:10px">
                <span style="width:50px;margin-right:10px">姓名</span>
                <el-input size="mini" v-model="search.xm" style="width:100px"/>
            </div>
            <div style="margin-right:10px">
                <span style="width:50px;margin-right:10px">联系电话</span>
                <el-input size="mini"  v-model="search.lxdh" style="width:100px"/>
            </div>
            <div style="margin-right:10px">
                <span style="width:50px;margin-right:10px">居住地址</span>
                <el-input size="mini"  v-model="search.jzdz" style="width:100px"/>
            </div>
            <div style="margin-right:10px">
                <span style="width:50px;margin-right:10px">标签编号</span>
                <el-input size="mini"  v-model="search.bqbh" style="width:100px"/>
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
            <el-table-column label="登记编号" prop="id" />
            <el-table-column label="登记日期" prop="djrq" width="160px">
                <template slot-scope="scope">
                    {{ $moment(scope.row.djrq).format('YYYY年M月D日 HH:mm') }}
                </template>
            </el-table-column>
            <el-table-column label="标签编号" prop="bqbh" />
            <el-table-column label="标签序号" prop="bqxh" />
            <el-table-column label="姓名" prop="xm" />
            <el-table-column label="性别" prop="xb">
                <template slot-scope="scope">
                    {{ getXb(scope.row.xb) }}
                </template>
            </el-table-column>
            <el-table-column label="年龄" prop="nl" />
            <el-table-column label="出生日期" prop="csrq" width="120px">
                <template slot-scope="scope">
                    {{ $moment(scope.row.csrq).format('YYYY年M月D日') }}
                </template>
            </el-table-column>
            <el-table-column label="居住地址" prop="jzdz" show-overflow-tooltip />
            <el-table-column label="联系电话" prop="lxdh" show-overflow-tooltip />
            <el-table-column label="身份证号" prop="zjhm" show-overflow-tooltip>
            </el-table-column>
            
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
import { getCheckInList } from '@/api'
export default {
  name: 'Dengji',
  data() {
      return {
          height: window.innerHeight - 280,
          list: [],
          search: {
              xm: '',
              lxdh: '',
              jzdz: '',
              bqbh: ''
          },
          pager: {
              count: 0,
              page:1,
              size:10
          }
      }
  },
  mounted() {
      this.doLoad()
  },
  methods: {
      doLoad() {
          getCheckInList(Object.assign(this.search, this.pager)).then(res=>{
              this.list = res.list
              this.pager.count = res.count
          })
      },
      getXb(v) {
          if (v == '1') {
              return '男'
          }else if (v == '2') {
              return '女'
          }else {
              return '未知'
          }
      },
      handleSizeChange(v) {
          this.pager.size = v;
          this.pager.page = 1;
          this.doLoad()
      },
      handleCurrentChange(v) {
          this.pager.page = v;
          this.doLoad()
      }
  }
}
</script>
<style scoped>

.box {
    margin-top:10px;

}
</style>