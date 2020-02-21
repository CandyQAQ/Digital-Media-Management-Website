import Vue from 'vue'
import Router from 'vue-router'
import MainPage from '@/components/MainPage'
import AnotherPage from '@/components/AnotherPage'
import CrawlPage from '@/components/CrawlPage'
import ImagePage from '@/components/ImagePage'
import Similarity from '@/components/Similarity'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'MainPage',
      component: MainPage
    },
    {
      path: '/noisy',
      name: 'AnotherPage',
      component: AnotherPage
    },
    {
      path: '/crawl',
      name: 'CrawlPage',
      component: CrawlPage
    },
    {
      path: '/image',
      name: 'ImagePage',
      component: ImagePage
    },
    {
      path: '/similarity',
      name: 'Similarity',
      component: Similarity
    }
  ]
})
