import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Social Plat Wiki",
  description: "A wiki for SocialPlat Project",
  head: [
    [
      'link', 
      { 
        rel: 'icon', 
        href: '/favicon.ico' 
      }
    ]
  ],
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Wiki', link: '/TEAM/team' }
    ],
    logo: '/favicon.ico',
    sidebar: [
      {
        text: '团队成员',
        items:  [
          { text: 'Team Members', link: '/TEAM/team'}
        ]
      },
      {
        text: '需求分析',
        items:  [
          { text: 'NABCD', link: '/NABCD'},
        ]
      },
      {
        text: 'API文档',
        items:  [
          { text: 'APIs', link: '/API/api-doc'}
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/MegaSuite/SocialPlat' }
    ]
  }
})