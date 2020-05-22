<template>
  <div class="row justify-content-center">
    <div class="row mb-5">
      <div class="col">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">学校占比：</h5>
            <apexchart type="pie" width="320" :options="pie.chartOptions" :series="pie.series"></apexchart>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">性别占比：</h5>
            <apexchart type="pie" width="320" :options="pie.chartOptions" :series="pie.series"></apexchart>
          </div>
        </div>
      </div>
    </div>

    <div class="row mb-5">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">新增：</h5>
          <apexchart type="area" width="710" :options="area.chartOptions" :series="area.series"></apexchart>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">总计：</h5>
          <apexchart type="area" width="710" :options="area.chartOptions" :series="area.series"></apexchart>
        </div>
      </div>
    </div>
  </div>
</template>

<script>


export default{
  name: 'overview',
  data () {
    return {
      area: {
          series: 
          [
            {
              name: 'User',
              data: [31, 40, 28, 51, 42, 109, 100]
            }, 
            {
              name: 'Post',
              data: [11, 32, 45, 32, 34, 52, 41]
            },
            {
              name: 'Comments',
              data: [12, 40, 28, 81, 42, 79, 90]
            }
          ],
          chartOptions: {
            chart: {
              height: 350,
              type: 'area'
            },
            dataLabels: {
              enabled: false
            },
            stroke: {
              curve: 'smooth'
            },
            xaxis: {
              type: 'datetime',
              categories: ["2018-09-19T00:00:00.000Z", "2018-09-19T01:30:00.000Z", "2018-09-19T02:30:00.000Z", "2018-09-19T03:30:00.000Z", "2018-09-19T04:30:00.000Z", "2018-09-19T05:30:00.000Z", "2018-09-19T06:30:00.000Z"]
            },
            tooltip: {
              x: {
                format: 'dd/MM/yy HH:mm'
              },
            },
          },
      },
      pie: {
          series: [44, 55, 13, 43, 22],
          chartOptions: {
            chart: {
              width: 380,
              type: 'pie',
            },
            labels: ['重庆邮电大学', '重庆大学', '重庆工商大学', '重庆第二师范', '重庆医科大学'],
            responsive: [{
              breakpoint: 480,
              options: {
                chart: {
                  width: 200
                },
                legend: {
                  position: 'bottom'
                }
              }
            }]
          }
      }
    }
  }
}

</script>