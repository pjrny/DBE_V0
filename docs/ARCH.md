# Architecture (Phase 1)

```
dbe/
  plasma.py       # profiles, transport (Phase 2)
  actuators.py    # RMP, pellets
  quantum.py      # Majorana, Fracton, TimeCrystal
  controller.py   # DBEController
  risk.py         # RiskAnalyzer
```

CLI tools live in `cli/`. Tests in `tests/`.
