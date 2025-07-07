[![Typing SVG](https://readme-typing-svg.demolab.com?font=Brass+mono&weight=800&size=25&pause=1000&color=F77522&vCenter=true&random=false&width=435&lines=Arbitrum+Nova)](https://git.io/typing-svg)
---
<img src="http://githubusercontent.alwayme.com/68747470733a2f2f-readme-typo.png" alt="." width="0" height="0">

This repository will allow you to create transactions on the **Arbitrum Nova**.

You can do **ETH -> USDC** exchange and vice versa, as well as wrap and unwrap ether.

The repository **supports** proxies.

## INSTALLATION

1. Install **Python 3.11+**.
2. `pip install -r requirements.txt`.
3. Paste the wallet private key in `accounts.txt` and set the settings in `settings.py`.

## SETTINGS

- `GAS_MULTIPLAYER` - GWEI multiplier [Integer].
- `USE_PROXY` - Proxy mode [Boolean].
- `RANDOM_WALLET` - Random wallet mode [Boolean].
- `SLIPPAGE` - Percentage that is lost on exchange [Integer].
- `SLEEP_FROM`, `SLEEP_TO` - Seconds to sleep after completing a task [Integer].
- `QUANTITY_THREADS` - Quantity threads [Integer].
- `THREAD_SLEEP_FROM`, `THREAD_SLEEP_TO` - Interval in seconds between thread starts [Integer].

In `all_modules.py`, you will be able to configure the minimum and maximum amount for each modules, as well as make your own list of modules to randomize actions.
