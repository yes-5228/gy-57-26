<template>
  <section class="view">
    <header class="view-header">
      <div>
        <p class="eyebrow">Reminders</p>
        <h2>课前提醒</h2>
      </div>
      <div class="filter-bar">
        <select v-model="filterStatus" @change="load">
          <option value="">全部状态</option>
          <option value="pending">待发送</option>
          <option value="sent">已发送</option>
          <option value="read">已阅读</option>
        </select>
      </div>
    </header>

    <section class="panel">
      <h3>即将开始的课程提醒</h3>
      <EmptyState v-if="upcoming.length === 0" text="暂无即将开始的课程" />
      <div v-else class="reminder-cards">
        <div v-for="item in upcoming" :key="item.id" class="reminder-card upcoming">
          <div class="reminder-icon">
            <BellRing :size="24" />
          </div>
          <div class="reminder-content">
            <div class="reminder-title">
              <strong>{{ item.student_name }}</strong> 的练车提醒
              <StatusBadge :status="item.status" />
            </div>
            <div class="reminder-details">
              <div class="detail-item">
                <Calendar :size="16" />
                <span>{{ formatDateTime(item.start_time) }} - {{ formatDateTime(item.end_time) }}</span>
              </div>
              <div class="detail-item">
                <User :size="16" />
                <span>教练：{{ item.coach_name }}</span>
              </div>
              <div class="detail-item">
                <Car :size="16" />
                <span>车辆：{{ item.car_no }}</span>
              </div>
            </div>
            <div class="reminder-actions">
              <button class="primary" :disabled="item.status !== 'pending'" @click="send(item.id)">
                <Send :size="16" />
                发送提醒
              </button>
              <button class="ghost" :disabled="item.status === 'read'" @click="markRead(item.id)">
                <Check :size="16" />
                标记已读
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="panel list-panel">
      <h3>全部提醒</h3>
      <EmptyState v-if="reminders.length === 0" />
      <table v-else>
        <thead>
          <tr>
            <th>训练时间</th>
            <th>学员</th>
            <th>教练</th>
            <th>车辆</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in reminders" :key="item.id">
            <td>{{ formatDateTime(item.start_time) }} - {{ formatDateTime(item.end_time) }}</td>
            <td>{{ item.student_name }}</td>
            <td>{{ item.coach_name }}</td>
            <td>{{ item.car_no }}</td>
            <td><StatusBadge :status="item.status" /></td>
            <td>
              <button
                class="primary"
                :disabled="item.status !== 'pending'"
                @click="send(item.id)"
                style="margin-right: 8px;"
              >
                <Send :size="16" />
                发送
              </button>
              <button class="ghost" :disabled="item.status === 'read'" @click="markRead(item.id)">
                <Check :size="16" />
                已读
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </section>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { BellRing, Calendar, Car, Check, Send, User } from 'lucide-vue-next'
import EmptyState from '../components/EmptyState.vue'
import StatusBadge from '../components/StatusBadge.vue'
import { reminderApi } from '../api/modules'
import { formatDateTime } from '../utils/date'

const props = defineProps({
  refreshToken: {
    type: Number,
    default: 0,
  },
})

const reminders = ref([])
const upcoming = ref([])
const filterStatus = ref('')

async function load() {
  const [all, upcomingList] = await Promise.all([
    filterStatus.value ? reminderApi.list().then(list => list.filter(r => r.status === filterStatus.value)) : reminderApi.list(),
    reminderApi.listUpcoming(24),
  ])
  reminders.value = all
  upcoming.value = upcomingList
}

async function send(id) {
  await reminderApi.send(id)
  await load()
}

async function markRead(id) {
  await reminderApi.read(id)
  await load()
}

onMounted(load)
watch(() => props.refreshToken, load)
</script>

<style scoped>
.filter-bar select {
  min-height: 40px;
  border: 1px solid #bcccdc;
  border-radius: 6px;
  padding: 8px 10px;
  background: #fff;
  color: #1f2933;
}

.reminder-cards {
  display: grid;
  gap: 14px;
}

.reminder-card {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 16px;
  padding: 16px;
  border: 1px solid #d9e2ec;
  border-radius: 8px;
  background: #fff;
}

.reminder-card.upcoming {
  border-left: 4px solid #0f766e;
  background: linear-gradient(to right, #f0fdfa, #ffffff);
}

.reminder-icon {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: #ccfbf1;
  color: #0f766e;
  border-radius: 8px;
  padding-top: 12px;
}

.reminder-content {
  display: grid;
  gap: 10px;
}

.reminder-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
}

.reminder-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 8px;
}

.detail-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #486581;
  font-size: 14px;
}

.reminder-actions {
  display: flex;
  gap: 10px;
  margin-top: 4px;
}
</style>
