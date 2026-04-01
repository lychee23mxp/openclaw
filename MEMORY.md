# MEMORY.md - Coco's Long-Term Memory

## NYU Email Backup

- **位置:** `/Users/lychees/.openclaw/workspace/nyu-email-backup/`
- **账号:** ys3848@nyu.edu
- **格式:** `.eml` 文件，按年/月/日分文件夹存放
- **备份完成日期:** 2026-03-31
- **总量:** 24,000+ 封邮件，约 3.4 GB
- **不含:** 垃圾邮件（Spam）和回收站（Trash）

### 搜索邮件

脚本位置: `/Users/lychees/.openclaw/workspace/scripts/search-email.sh`

```bash
# 搜关键词
./scripts/search-email.sh "关键词"

# 只搜主题
./scripts/search-email.sh "financial aid" --subject

# 按发件人过滤
./scripts/search-email.sh "作业" --from professor@nyu.edu

# 显示更多结果
./scripts/search-email.sh "registration" --limit 20
```

或者直接告诉 Coco 要找什么，Coco 来搜。

---

## GitHub 贡献

- **账号:** lychee23mxp / ys3848@nyu.edu
- **仓库:** https://github.com/lychee23mxp/openclaw
- **每日自动提交:** 凌晨 3 点 + 早上 6 点（crontab）
- **脚本:** `/Users/lychees/.openclaw/workspace/scripts/daily-sync.sh`
- 之前提交用的是 `coco@openclaw`，不计入 GitHub 贡献，已修复

---

## 关于 Lychee

- **GitHub:** lychee23mxp
- **NYU 邮箱:** ys3848@nyu.edu
- **个人 Gmail:** lylashangll@gmail.com
- **时区:** America/New_York
