<script setup lang="ts">
const props = defineProps<{
  cards: {
    title: string
    details?: string
    link?: string
    links?: { text: string; href: string }[]
    sections?: { details: string; link: string; linkText: string }[]
    wide?: boolean
  }[]
  columns?: number
}>()
</script>

<template>
  <div
    class="card-grid"
    :style="props.columns !== undefined ? { gridTemplateColumns: `repeat(${props.columns}, 1fr)` } : {}"
  >
    <template v-for="card in props.cards" :key="card.title">
      <a v-if="card.link" :href="card.link" class="card" :class="{ 'card--wide': card.wide }">
        <h3 class="card-title">{{ card.title }}</h3>
        <p class="card-details">{{ card.details }}</p>
      </a>
      <div v-else-if="card.sections" class="card card--wide">
        <h3 class="card-title">{{ card.title }}</h3>
        <div class="card-sections">
          <template v-for="(section, i) in card.sections" :key="i">
            <div v-if="i > 0" class="card-sections-divider"></div>
            <div class="card-section">
              <p class="card-details">{{ section.details }}</p>
              <a :href="section.link" class="card-link">→ {{ section.linkText }}</a>
            </div>
          </template>
        </div>
      </div>
      <div v-else class="card" :class="{ 'card--wide': card.wide }">
        <h3 class="card-title">{{ card.title }}</h3>
        <div v-if="card.wide && card.links" class="card-wide-body">
          <p class="card-details">{{ card.details }}</p>
          <div class="card-links card-links--side">
            <a v-for="l in card.links" :key="l.href" :href="l.href" class="card-link">{{ l.text }}</a>
          </div>
        </div>
        <template v-else>
          <p class="card-details">{{ card.details }}</p>
          <div v-if="card.links" class="card-links">
            <a v-for="l in card.links" :key="l.href" :href="l.href" class="card-link">{{ l.text }}</a>
          </div>
        </template>
      </div>
    </template>
  </div>
</template>

<style scoped>
.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: 1fr;
  gap: 16px;
  margin: 16px 0;
}

@media (max-width: 640px) {
  .card-grid {
    grid-template-columns: 1fr !important;
  }
}

.card {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 20px 24px;
  background-color: var(--vp-c-bg-soft);
  text-decoration: none;
  transition: border-color 0.25s ease, background-color 0.25s ease;
}

.card:hover {
  border-color: var(--vp-c-brand-1);
  background-color: var(--vp-c-bg-soft-up);
  text-decoration: none;
}

.card--wide {
  grid-column: span 2;
}

.card-title {
  margin: 0 0 8px;
  font-size: 16px;
  font-weight: 600;
  color: var(--vp-c-brand-1);
  line-height: 24px;
  border: none;
}

.card-details {
  margin: 0;
  font-size: 14px;
  font-weight: 500;
  color: var(--vp-c-text-2);
  line-height: 22px;
}

/* sections layout (option 2) */
.card-sections {
  display: flex;
  flex: 1;
}

.card-section {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-section .card-details {
  flex: 1;
}

.card-sections-divider {
  width: 1px;
  background: var(--vp-c-divider);
  margin: 0 20px;
  flex-shrink: 0;
}

.card-link {
  margin-top: 12px;
  font-size: 14px;
  font-weight: 600;
  color: var(--vp-c-brand-1);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
}

/* wide body layout (original) */
.card-wide-body {
  display: flex;
  flex-direction: row;
  gap: 0;
  flex: 1;
}

.card-wide-body .card-details {
  flex: 1;
  padding-right: 24px;
}

.card-links {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--vp-c-divider);
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.card-links--side {
  margin-top: 0;
  padding-top: 0;
  border-top: none;
  border-left: 1px solid var(--vp-c-divider);
  padding-left: 24px;
  min-width: 200px;
  justify-content: center;
}

.card-links .card-link {
  margin-top: 0;
}

.card-links .card-link::before {
  content: '→ ';
}

@media (max-width: 640px) {
  .card--wide {
    grid-column: span 1;
  }

  .card-sections {
    flex-direction: column;
  }

  .card-sections-divider {
    width: unset;
    height: 1px;
    margin: 16px 0;
  }

  .card-wide-body {
    flex-direction: column;
  }

  .card-wide-body .card-details {
    padding-right: 0;
  }

  .card-links--side {
    border-left: none;
    border-top: 1px solid var(--vp-c-divider);
    padding-left: 0;
    padding-top: 12px;
    margin-top: 12px;
    min-width: unset;
    justify-content: flex-start;
  }
}
</style>
