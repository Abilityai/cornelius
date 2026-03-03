---
created: '2026-01-11'
updated: '2026-03-03'
tags:
- anytype-import
- note
type: permanent
source_type: note
anytype_id: bafyreifnibsxmqo422ky5hfd6zxgoc4s4ym6sypyvyakzjqygbh6bvburu
created_by: human
updated_by: claude-opus-4-6
agent_version: '02.25'
---
Include in Claude.md   
   
- Tdd approach   
- Context management:   
- Print minimal, actionable error messages. If you have a thousand tests,   
- [don't print "test passed" a thousand times](https://www.humanlayer.dev/blog/context-efficient-backpressure)   
- . That's satisfying/reassuring for humans, but for the model you just want "1000/1000 success" and exit code zero. If a test fails, print the assertion that failed, maybe a call stack, actionable information the model can use to fix the problem.   
- For Python specifically,   
- [uv](https://docs.astral.sh/uv/)   
- is the best thing ever created. Before we had virtualenvs and all that mess. Now it's just uv run   
- [main.py](https://main.py/)   
- and you tell the model "we're using uv in this project" and it knows. It was designed with this kind of workflow in mind.   
- Hard requirement: your project has to build, test, and lint with a single command. No README that says "pass this flag" or "set this library path manually." Put that in a configuration file once and make the single-command thing work.   
   
   
