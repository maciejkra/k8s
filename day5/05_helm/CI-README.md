Split all components

- Code build
- Image build
- Image tag * push
- Yaml generation
- Yaml update


Allow any part of CI pipeline to be executed as separate task

examples:
 - I want to deploy same code, but with different infrastructure
 - I want to deploy different code, but with same infrastructure
 - I want to deploy both new code & infrastructure


- Keep image tag together with release
- Be carefull with policies