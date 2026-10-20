# Candidate questions to review

To approve an item, set its "status" in eval/candidates.json to "approved" (or "rejected"), then run python3 promote_candidates.py.

| ID | Type | Role | Gold page | Question | Key facts |
|---|---|---|---|---|---|
| 1 | generated-factual | all | HR-001 p1 | What time does the normal workday begin and end at our company? | 9:00, 17:30 |
| 2 | generated-factual | all | HR-001 p1 | During which part of the day am I expected to be available for working with teammates? | 10:00, 15:00 |
| 3 | generated-factual | all | HR-001 p1 | How many vacation days do I get each year if I work full time? | 22 days |
| 4 | generated-factual | all | HR-001 p1 | If I don't use all of my time off this year, how much can I roll over into next year? | 5 days |
| 5 | generated-factual | all | HR-001 p2 | What's the maximum number of days I can work from home each week, and do I need anyone's permission? | 3 days, manager approval |
| 6 | generated-factual | all | HR-001 p2 | When do I need to record the days I worked remotely, and where do I do it? | Friday noon, attendance tool |
| 7 | generated-factual | all | HR-001 p2 | If I'm the main person taking care of a new baby, how much time off with pay can I get? | 16 weeks |
| 8 | generated-factual | all | HR-001 p2 | Does the company pay me while I'm out on leave after having a child if I'm the primary caregiver? | paid, 16 weeks |
| 9 | generated-factual | hr | HR-002 p1 | What is the pay range for a Product Manager at our company? | L4, 115,000, 140,000 |
| 10 | generated-factual | hr | HR-002 p1 | How much can someone in a Senior Analyst role expect to earn, and which level is that? | L3, 95,000, 115,000 |
| 11 | generated-factual | hr | HR-002 p2 | When do managers go over yearly pay raises for employees? | March |
| 12 | generated-factual | hr | HR-002 p2 | How big is the bonus I can aim for if I'm at the L5 level? | 15 percent, base salary |
| 13 | generated-factual | finance | FIN-002 p1 | How much can I claim per day for food when I travel within the country? | 90 USD, per day |
| 14 | generated-factual | finance | FIN-002 p1 | At what amount do I need to keep a receipt for a meal expense? | 30 USD, above |
| 15 | generated-factual | finance | FIN-002 p2 | How long do I have after buying something for work to turn in my expense report? | 45 days |
| 16 | generated-factual | finance | FIN-002 p2 | Can I still file a claim dated after the start of March 2026 using the older version of the expense policy? | v2, superseded, 1 March 2026 |
| 17 | generated-factual | finance | FIN-003 p1 | I need to give a customer a 1,500 dollar refund. Who has to sign off on it? | Finance Manager, 200 to 2,000 |
| 18 | generated-factual | finance | FIN-003 p1 | What's the biggest refund a Support Lead can okay without escalating, and when does it have to go to the CFO? | 200 USD, 2,000 USD, CFO |
| 19 | generated-factual | finance | TRV-001 p1 | I'm flying to a meeting that's about 4 hours away. Can I book business class, or do I have to fly coach? | economy, 6 hours |
| 20 | generated-factual | finance | TRV-001 p1 | What's the most I can spend on a hotel room per night when traveling to another city within the country? | 220 USD, per night, domestic |
| 21 | generated-factual | security | SEC-001 p1 | How long can I keep elevated admin rights on a system before someone has to sign off on them again? | 90 days, re-approved |
| 22 | generated-factual | security | SEC-001 p1 | Is it okay for my team to share one login for a production server, and what kind of sign-in checks are needed there? | Shared accounts are prohibited, multi-factor authentication |
| 23 | generated-factual | security | SEC-001 p2 | How often do system owners have to go back and check who has access to their systems? | quarterly, system owners |
| 24 | generated-factual | security | SEC-001 p2 | After someone leaves the company, what's the deadline for shutting off their system access? | 24 hours |
| 25 | generated-factual | security | SEC-002 p1 | How quickly does someone need to respond once a top-priority security incident is raised? | 15 minutes |
| 26 | generated-factual | security | SEC-002 p1 | If we confirm that customer data was exposed, how soon does the CISO have to be told, and who is responsible for telling them? | 1 hour, incident commander |
| 27 | generated-factual | security | SEC-002 p2 | How soon after a security incident does the team have to finish the review of what happened? | 5 business days |
| 28 | generated-factual | security | SEC-002 p2 | When we go over an incident afterward, is anyone going to be blamed or disciplined for what went wrong? | blameless |
| 29 | generated-factual | security | ENG-001 p1 | How far back can I look at old chats and calls with customers before they get purged? | 18 months |
| 30 | generated-factual | security | ENG-001 p1 | What's the timeframe for keeping our accounting and money-related documents, and how soon do backup copies get wiped? | 7 years, 35 days |
| 31 | generated-factual | all | PRD-001 p1 | How quickly do enterprise customers get an initial reply from support after opening a ticket? | 1 hour, enterprise |
| 32 | generated-factual | all | PRD-001 p1 | What's the goal for getting a standard support ticket fully resolved? | 3 business days |
| 33 | generated-factual | all | PRD-001 p2 | What level of service availability do we promise to our biggest clients each month? | 99.9 percent, calendar month |
| 34 | generated-factual | all | PRD-001 p2 | Do our largest accounts get their own way to reach support, or do they share the general line? | dedicated support channel |
| 35 | generated-factual | all | PRD-002 p1 | How often do we push out new releases, and on what day of the week? | every second Tuesday |
| 36 | generated-factual | all | PRD-002 p1 | What checks does a build have to clear before it can go out the door? | automated tests, security scan, product owner |
| 37 | generated-factual | all | PRD-002 p2 | Who do I need to get sign-off from if I want to push an urgent fix to production without waiting for the normal release schedule? | on-call engineering manager |
| 38 | generated-factual | all | PRD-002 p2 | If my code change affects billing, is there a specific mechanism I'm required to use when rolling it out? | Feature flags |
| 39 | generated-factual | all | PRD-003 p1 | What topics do I need to cover when putting together a PRD? | problem statement, target user, success metrics, non-goals, risks |
| 40 | generated-factual | all | PRD-003 p1 | Is there a step I need to complete before a product can be launched? | readiness review |
| 41 | generated-refusal | all | none (refuse) | What is the guest Wi-Fi password at the Denver office? | - |
| 42 | generated-refusal | all | none (refuse) | What is on the cafeteria lunch menu this week? | - |
| 43 | generated-refusal | all | none (refuse) | What is the company's revenue forecast for 2027? | - |
| 44 | generated-refusal | all | none (refuse) | Who won the Employee of the Year award in 2025? | - |
| 45 | generated-refusal | all | none (refuse) | What is the roadmap and launch date for the mobile app's next major version? | - |
| 46 | generated-refusal | all | none (refuse) | How do I file a patent application for something I invented at work? | - |
| 47 | generated-refusal | all | none (refuse) | When and where is the next company-wide offsite being held? | - |
| 48 | generated-refusal | all | none (refuse) | Which vendor does the company use for payroll processing? | - |
