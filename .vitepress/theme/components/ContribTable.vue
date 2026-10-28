<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  rows: (
    | { title: string; details: string; link: string; grouped?: boolean }
    | { groupLabel: string }
  )[]
}>()

type TopLevelRow = { type: 'row'; title: string; details: string; link: string }
type Group = { type: 'group'; id: string; label: string; rows: { title: string; details: string; link: string }[] }

const sections = computed(() => {
  const result: (TopLevelRow | Group)[] = []
  let currentGroup: Group | null = null

  for (const row of props.rows) {
    if ('groupLabel' in row) {
      currentGroup = {
        type: 'group',
        id: `contrib-group-${row.groupLabel.toLowerCase().replace(/\s+/g, '-')}`,
        label: row.groupLabel,
        rows: [],
      }
      result.push(currentGroup)
    } else if (row.grouped && currentGroup) {
      currentGroup.rows.push(row)
    } else {
      currentGroup = null
      result.push({ type: 'row', ...row })
    }
  }

  return result
})
</script>

<template>
  <div class="contrib-table" role="list">
    <template v-for="section in sections" :key="section.type === 'row' ? section.link : section.label">
      <a
        v-if="section.type === 'row'"
        :href="section.link"
        class="contrib-table-row"
        role="listitem"
      >
        <span class="contrib-table-title">{{ section.title }}</span>
        <span class="contrib-table-details">{{ section.details }}</span>
      </a>
      <div
        v-else
        class="contrib-table-group"
        role="group"
        :aria-labelledby="section.id"
      >
        <div :id="section.id" class="contrib-table-label">{{ section.label }}</div>
        <a
          v-for="row in section.rows"
          :key="row.link"
          :href="row.link"
          class="contrib-table-row contrib-table-row--grouped"
          role="listitem"
        >
          <span class="contrib-table-title">{{ row.title }}</span>
          <span class="contrib-table-details">{{ row.details }}</span>
        </a>
      </div>
    </template>
  </div>
</template>

<style scoped>
.contrib-table {
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  overflow: hidden;
  margin: 16px 0;
  background: var(--vp-c-bg);
}


.contrib-table-group {
  display: contents;
}

.contrib-table-label {
  padding: 6px 20px;
  font-size: 11px;
  font-weight: 700;
  color: var(--vp-c-text-2);
  text-transform: uppercase;
  letter-spacing: 0.07em;
  background: var(--vp-c-bg);
  border-top: 1px solid var(--vp-c-divider);
}

.contrib-table-row {
  display: flex;
  gap: 20px;
  padding: 14px 20px;
  border-top: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  text-decoration: none;
  transition: background-color 0.25s ease;
}

.contrib-table-row:first-child {
  border-top: none;
  border-radius: 11px 11px 0 0;
}

.contrib-table > a:last-child {
  border-radius: 0 0 11px 11px;
}

/* no line between the group label and first grouped row */
.contrib-table-label + .contrib-table-row {
  border-top: none;
}

/* no lines between consecutive grouped rows */
.contrib-table-row--grouped + .contrib-table-row--grouped {
  border-top: none;
}

.contrib-table-row:hover {
  background: var(--vp-c-bg-soft);
}

.contrib-table-row:focus-visible {
  outline: 4px auto -webkit-focus-ring-color;
  outline-offset: -2px;
}

.contrib-table-row--grouped {
  padding-left: 32px;
}

.contrib-table-title {
  min-width: 190px;
  font-size: 14px;
  font-weight: 600;
  color: var(--vp-c-brand-1);
  flex-shrink: 0;
}

.contrib-table-details {
  font-size: 14px;
  color: var(--vp-c-text-2);
  line-height: 22px;
  flex: 1;
}

@media (max-width: 640px) {
  .contrib-table-row {
    flex-direction: column;
    gap: 6px;
  }

  .contrib-table-row--grouped {
    padding-left: 20px;
  }

  .contrib-table-title {
    min-width: unset;
  }
}
</style>
