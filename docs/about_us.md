---
hide_toc: true
---

# About Us

### Capgemini Invent combines strategy, technology, data science and creative design to solve the most complex business and technology challenges.

Disruption is not new, but the pace of change is. The fourth industrial revolution is forcing businesses to rethink everything they know.

Leading organizations behave as living entities, constantly adapting to change. With invention at their core, they continuously redesign their business to generate new sources of value. Winning is about fostering inventive thinking to create what comes next.

### Invent. Build. Transform.

This is why we have created Capgemini Invent, Capgemini’s new digital innovation, consulting and transformation global business line. Our multi-disciplinary team helps business leaders find new sources of value. We accelerate the process of turning ideas into prototypes and scalable real-world solutions; leveraging the full business and technology expertise of the Capgemini Group to implement at speed and scale.

The result is a coordinated approach to transformation, enabling businesses to create the products, services, customer experiences, and business models of the future.

## We're Hiring!

<div class="termy">

```console
$ pip install capgemini_invent.job_desc
---> 100%
open_positions installed!

$ pip install resume
---> 100%
resume installed!
```

</div>


```python
import time
import datetime
import requests
import resume
import capgemini_invent.job_desc as JD

on_it = (datetime.datetime.now() + datetime.timedelta(days=1)).total_seconds()

with open(JD, "r") as jd:
    thoughts = jd.read()
    time.sleep(on_it)
    if thoughts == "Thats for me!":
        latest_resume = {"resume": (resume.latest, open(resume.latest, "rb"))}
        requests.post(JD.reply, files=latest_resume)
        quit()
    else:
        print("No worries! Become a contributor to our open source projects")

```


Do you want to be part of the team that builds doc_loader and [other great products](https://github.com/CapgeminiInventIDE) at Capgemini Invent? If so, you're in luck! Capgemini Invent is currently hiring Data Scientists who love using data to drive their decisions. Take a look at [our open positions](https://www.capgemini.com/careers/job-search/?search_term=capgemini+invent) and see if you're a fit.
