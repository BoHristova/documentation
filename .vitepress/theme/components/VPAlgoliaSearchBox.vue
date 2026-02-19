<script setup lang="ts">
/*
MIT License

Copyright (c) 2019-present, Yuxi (Evan) You

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Copied and adapted from -> https://github.com/vuejs/vitepress/blob/2342269486e82b9b3f692976892f77b0792268ee/src/client/theme-default/components/VPAlgoliaSearchBox.vue

*/


import docsearch from '@docsearch/js'
import {useRouter, withBase} from 'vitepress'
import type { DefaultTheme } from 'vitepress/theme'
import { nextTick, onMounted, watch } from 'vue'
import { useData } from 'vitepress'

const props = defineProps<{
  algolia: DefaultTheme.AlgoliaSearchOptions
}>()

const router = useRouter()
const { site, localeIndex, lang } = useData()

type DocSearchProps = Parameters<typeof docsearch>[0]

onMounted(update)
watch(localeIndex, update)

async function update() {
  await nextTick()
  const options = {
    ...props.algolia,
    ...props.algolia.locales?.[localeIndex.value]
  }
  const rawFacetFilters = options.searchParameters?.facetFilters ?? []
  const facetFilters = [
    ...(Array.isArray(rawFacetFilters)
            ? rawFacetFilters
            : [rawFacetFilters]
    ).filter((f) => !f.startsWith('lang:')),
    `lang:${lang.value}`
  ]
  initialize({
    ...options,
    searchParameters: {
      ...options.searchParameters,
      facetFilters
    }
  })
}

function initialize(userOptions: DefaultTheme.AlgoliaSearchOptions) {
  const options = Object.assign<
      {},
      DefaultTheme.AlgoliaSearchOptions,
      Partial<DocSearchProps>
  >({}, userOptions, {
    container: '#docsearch',

    navigator: {
      navigate({ itemUrl }) {
        router.go(itemUrl)
      }
    },

    transformItems(items) {
      return items.map((item) => {
        const breadcrumbValue = item.breadcrumb || item.hierarchy.lvl0;
        return Object.assign({}, item, {
          url: getRelativePath(item.url),
          hierarchy: {
            ...item.hierarchy,
            lvl0: breadcrumbValue
          },
          _highlightResult: {
            ...item._highlightResult,
            hierarchy: {
              ...item._highlightResult.hierarchy,
              lvl0: {
                ...item._highlightResult.hierarchy.lvl0,
                value: breadcrumbValue
              }
            }
          }
        })
      })
    }
  }) as DocSearchProps

  docsearch(options)
}

function getRelativePath(url: string) {
  const { pathname, hash } = new URL(url, location.origin)
  return withBase(pathname).replace(/\.html$/, site.value.cleanUrls ? '' : '.html') + hash
}
</script>

<template>
  <div id="docsearch" />
</template>
