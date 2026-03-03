---
created: '2026-01-10'
updated: '2026-03-03'
tags:
- anytype-import
- project
type: permanent
source_type: project
anytype_id: bafyreih6qx4bdvfmsyxy5w2giaotyorucvnhfyqwxq7rc7ghspttsom7sa
created_by: human
updated_by: claude-opus-4-6
agent_version: '02.25'
local_path: /Users/jlb/Documents/Projects/Personal/gatsby-wedding
status: Shelved
---
# gatsby-wedding   
gatsby version of startbootstrap-agency with i18n supported.   
![badge-success.svg"; filename*=UTF-8''badge-success](attachments/anytype-import/badge-success-svg-filename-utf-8badge-success.svg)    
**This project is migrated to Gatsby@v4**   
- check the latest Gatsby@v3 version [here](https://github.com/thundermiracle/gatsby-startbootstrap-agency/tree/gatsby-3).   
- check the latest Gatsby@v2 version [here](https://github.com/thundermiracle/gatsby-startbootstrap-agency/tree/gatsby-2.0).   
   
## Preview   
[startbootstrap-agency](files/startbootstrap-agency.png)    
## Sample page   
[https://gatsby-startbootstrap-agency.netlify.app](https://gatsby-startbootstrap-agency.netlify.app)   
[https://gatsbystartbootstrapagency1.gatsbyjs.io/](https://gatsbystartbootstrapagency1.gatsbyjs.io/)   
[※ startbootstrap-agency (Original Version)](https://github.com/BlackrockDigital/startbootstrap-agency)   
[※ startbootstrap-agency-webpack(Webpack Version)](https://github.com/thundermiracle/startbootstrap-agency-webpack/)   
## Note   
If you're not interesting in i18n, use **[StaticQueryVersion](https://github.com/thundermiracle/gatsby-startbootstrap-agency/tree/StaticQueryVersion) instead. StaticQueryVersion gets better performance and better code structure.**   
## How to use   
This project is using `yarn` as the package manager. You have to set yarn as Gatsby-cli's package manager first.   
[https://www.gatsbyjs.com/docs/glossary/yarn/#using-yarn-as-your-gatsby-package-manager](https://www.gatsbyjs.com/docs/glossary/yarn/#using-yarn-as-your-gatsby-package-manager)   
```
npm install -g gatsby-cli

gatsby new my-blog-folder https://github.com/thundermiracle/gatsby-startbootstrap-agency

```
## Why Gatsby Version   
1. Using Gatsby could tree-shaking unnecessary code, optimizing images which make first contentful paint very fast.   
    > Original version is great but have to load too many unnecessary contents from CDN including all components in bootstrap, all solid & brands icons in fontawesome. That dramatically slows down the FCP(first contentful paint) in 3G environment.   

2. i18n is really easy in Gatsby and i18n is more maintainable.   
    > Implementation of i18n in original version is not easy and will make a lot of redundant code.   

   
## Comparison of Original, Webpack and Gatsby version   
### Gatsby Version   
[lighthouse_gatsby](files/lighthouse_gatsby.png)    
### Webpack Version   
[lighthouse_webpack](files/lighthouse_webpack.png)    
### Original Version   
[lighthouse_original](files/lighthouse_original.png)    
## Basic Configuration   
- `iconName` in Services.md MUST be defined in `'config/CustomIcons.jsx'`.   
- `imageFileName` in markdown MUST be added in `'content/assets'`.   
- all configurable contents are saved in markdown files in `'content'` folder.   
- change `file name's number` in `'content/sections'` folder to change the sort order.   
- nullable items (if defined):   
    - `anchor` in section markdown: display in menu if defined in sections' markdown   
    - items in `social`: `twitter, facebook, linkedin, github, medium`   
    - `jumpToAnchor, jumpToAnchorText` in Top.md: add button in Top section   
   
## i18n Configuration   
- set defaultLang in `'config/site.js'`   
- add langTextMap to `'config/site.js'` (LanguageSelector won't display if langTextMap is not defined. Consider using StaticQueryVersion if i18n is not necessary)   
- copy markdown files in `'content'` folder, rename it to `xxxx.[langKey].md` and translate the contents   
   
## License   
This project is licensed under the terms of the [[/License]].   
