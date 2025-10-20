# Intelligent Agents Module - Reflective Piece

### WHAT? - Description of Experience

This module's central focus was a multi-agent email forensics system, developed first as a team project in Unit 6 with Andrea Trevisi and Pavlos Papachristos, then extended individually in Unit 11.

The module began exploring intelligent agent architectures, particularly the contrast between Brooks' (1991) reactive agents and Bratman et al.'s (1988) deliberative BDI model. Discussion 1 examined how agent-based systems enable bottom-up simulation of emergent phenomena, providing virtual laboratories for organizational strategy testing (Bonabeau, 2002).

Learning agent communication through Searle's (1969) speech act theory became practical in Unit 6, where I implemented KQML dialogue protocols (Finin et al., 1994) between procurement and warehouse agents. The team project applied these principles to email forensics. My specific contributions included merging team code into a cohesive architecture, restructuring Pavlos's visualization into a DashboardAgent class, embedding charts in HTML reports, drafting the project report, and creating UML diagrams documenting system architecture.

Discussion 2 explored how modern word embeddings (Mikolov et al., 2013) address the ontology dependence problem that limits classical agent communication languages. Unit 8 revealed natural language complexity through constituency parsing and structural ambiguity. Discussion 3 and Unit 10 examined deep learning's productivity implications (World Economic Forum, 2022) and ethical concerns in generative AI.

My individual project in Unit 11 extended the team foundation, influenced by Industry 4.0 applications research (Wang et al., 2016). I restructured the architecture into a four-agent pipeline (DiscoveryAgent, AnalysisAgent, DashboardAgent, ReportAgent) with explicit design patterns: Repository for data access abstraction, Strategy for pluggable detection methods, Factory for visualization generation, and Template Method for report structure. The implementation included 29 comprehensive tests (25 unit tests validating individual methods, 3 integration tests ensuring agent coordination, and 1 end-to-end test validating the complete pipeline), all achieving 100% pass rate. The system demonstrated autonomous operation where agents discover data, analyze threats using four parallel strategies (keyword, temporal, source, volume), generate eight visualization types, and produce both technical and executive reports without human intervention. Critical attention went to error handling, with tests validating graceful degradation for corrupted files and malformed data. This demonstrated progression from team collaboration to independent mastery of production-quality multi-agent development.

### SO WHAT? - Analysis and Interpretation

#### Emotional Response and Behavioral Analysis

The team project presented coordination challenges. Working across time zones with Andrea and Pavlos required adapting to asynchronous communication. When merging Pavlos's analytics dashboard, I discovered incompatible data formats between agents. This integration challenge became a valuable learning opportunity, revealing through Rolfe et al.'s (2001) framework how technical problem-solving and team coordination must work together.

The integration work became productive when I refactored Pavlos's visualizations into a proper DashboardAgent class with clear contracts. Reading Fowler's (2018) while experiencing this practical challenge made abstract principles concrete. Creating UML diagrams for the report further solidified my understanding, as visualizing agent interactions exposed communication patterns and data flow requirements.

The individual project built confidence through incremental validation. Implementing 29 tests initially felt extensive, but each passing test confirmed design decisions. When tests caught type mismatches and edge cases, they validated the investment in comprehensive testing. This experience transformed my approach, making test-driven development integral rather than optional.

Reflecting on my behavior, I recognize a tendency toward technical optimization when facing design choices. Engaging with Sommer & Paxson's (2010) research on machine learning for intrusion detection helped me understand that the rule-based versus machine learning decision involved genuine trade-offs between interpretability and adaptability, not a simple preference.

#### What Produced My Learning

The contrast between Brooks' (1991) reactive and Bratman et al.'s (1988) deliberative BDI models became real when implementing agents. Deciding whether AnalysisAgent should react immediately to keywords or maintain state to track patterns transformed theoretical concepts into practical design choices.

The module's structure built complexity gradually. Unit 6's KQML dialogue established foundations. The team project added coordination challenges. The individual project required comprehensive testing and documentation. Each step built on the previous without being overwhelming.

The most significant learning came through encountering problems. When integration testing revealed agent communication failures, I had to trace data flow through the system and examine my assumptions about format compatibility. This failure taught me more about interface design than successful implementations would have.

Reading sequence influenced understanding. Encountering word embeddings (Mikolov et al., 2013) after working with rigid speech act protocols showed how learned representations can address ontology limitations. Reading Industry 4.0 systems research (Wang et al., 2016) before implementing my project connected academic concepts to real applications.

#### Evidence of Skills and Knowledge Developed

Agent system design evolved measurably. The four-agent pipeline implementing Repository, Strategy, Factory, and Template Method patterns (Wooldridge, 2009) now transfers to distributed systems and microservices. I've already applied this to another project, decomposing monolithic code into independent services.

Testing sophistication grew from zero to production-standard. The 29 automated tests (25 unit, 3 integration, 1 end-to-end, 100% passing) demonstrate systematic validation. Test-driven development caught integration issues early that would have silently failed in production.

Critical evaluation developed through honest limitation assessment. Acknowledging our rule-based system sacrificed adaptability for interpretability (Sommer & Paxson, 2010) required moving beyond rationalization. Contextualizing this trade-off with contemporary research (Verma & Das, 2022) positioned work within broader landscapes.

Team collaboration grew through real coordination challenges. Cross-timezone communication, version control conflicts, and design negotiation developed essential distributed team skills evidenced by successful delivery despite geographical dispersion.

Ethical awareness emerged through Unit 10 readings (World Economic Forum, 2022) and Discussion 3. Recognizing technical capability advances faster than governance (European Parliament, 2024; NIST, 2023) now informs my approach. I proactively consider bias, privacy, and transparency before implementation.

### NOW WHAT? - Action Plan and Future Application

#### Immediate Applications

Testing discipline is now non-negotiable. Every project begins with test infrastructure. Modular design principles guide problem decomposition regardless of domain. Ethical consideration is front-loaded: I analyze biases, privacy, and societal impacts before implementation.

#### Professional Development Roadmap (6-12 Months)

**Model Context Protocol Integration:** I am currently analyzing implementing the Model Context Protocol (MCP) to enable multi-agent intercommunication across enterprise tools. The goal is to develop agents that can coordinate between Jira dashboards, Salesforce tickets, and Slack, automating Standard Operating Procedures (SOPs) from our Site Reliability Engineering team. This applies the multi-agent coordination principles from this module to real operational workflows, where autonomous agents handle routine tasks while escalating complex issues to human operators.

**Scaling Agent Systems to Production:** Drawing on Wang et al.'s (2016) Industry 4.0 coordination mechanisms, I'm exploring how to scale from the module's 50-email demonstrations to enterprise-scale deployment processing thousands of operational events. This involves distributed agent architectures, message queues for inter-agent communication, and implementing the interface design principles learned through this module's integration challenges.

#### Areas for Continued Development

**Advanced Agent Communication:** Moving beyond KQML/KIF to modern protocols like MCP requires deeper understanding of how agents negotiate shared context dynamically, building on Discussion 2's insights about learned representations versus rigid ontologies.

**Production-Ready Error Handling:** The graceful error handling validated in testing (corrupted files, malformed data) needs expansion for production environments where agent failures must be logged, reported, and self-healed without human intervention.

**Cross-Platform Integration:** Connecting heterogeneous systems (Jira, Salesforce, Slack) requires mastering API integration, authentication patterns, and data transformation between different organizational tools, extending the interface design principles learned in the team project.

---

## References

Bonabeau, E. (2002) Agent-based modeling: Methods and techniques for simulating human systems. *Proceedings of the National Academy of Sciences*, 99(suppl 3): 7280-7287.

Bratman, M.E., Israel, D.J. and Pollack, M.E. (1988) Plans and resource-bounded practical reasoning. *Computational Intelligence*, 4(3): 349–355.

Brooks, R.A. (1991) Intelligence without representation. *Artificial Intelligence*, 47(1–3): 139–159.

Casey, E. (2011) *Digital evidence and computer crime: Forensic science, computers, and the internet*. 3rd ed. London: Academic Press.

European Parliament. (2024) *EU AI Act: first regulation on artificial intelligence*. Available from: https://www.europarl.europa.eu/news/en/headlines/society/20230601STO93804/eu-ai-act-first-regulation-on-artificial-intelligence [Accessed 7 October 2025].

Finin, T., Weber, J., Wiederhold, G., Genesereth, M., Fritzson, R., McKay, D., McGuire, J., Pelavin, R., Shapiro, S. and Beck, C. (1994) 'KQML as an agent communication language', in *Proceedings of the third international conference on Information and knowledge management*, pp. 456-463.

Foit, K. (2022) 'Agent-based Modelling of Manufacturing Systems in the Context of "Industry 4.0"', *Journal of Physics: Conference Series*, 2198(1), pp. 1–10.

Forbes (2015) *Microsoft's Deep Learning Project Outperforms Humans In Image Recognition*. Available at: https://www.forbes.com/sites/michaelthomsen/2015/02/19/microsofts-deep-learning-project-outperforms-humans-in-image-recognition/

Fowler, M. (2018) *Refactoring: Improving the Design of Existing Code*. 2nd ed. Boston: Addison-Wesley Professional.

Hearst, M.A. (1992) 'Automatic acquisition of hyponyms from large text corpora', in *COLING 1992 Volume 2: The 14th International Conference on Computational Linguistics*.

Kaelbling, L.P. (1991) 'A situated-automata approach to the design of embedded agents', *ACM SIGART Bulletin*, 2(4), pp. 85–88.

Maes, P. (1991) 'The agent network architecture (ANA)', *ACM SIGART Bulletin*, 2(4), pp. 115–120.

Mikolov, T., Chen, K., Corrado, G. and Dean, J. (2013) 'Distributed representations of words and phrases and their compositionality', *Advances in neural information processing systems*, pp. 1–9.

NIST (2023) *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. Available from: https://www.nist.gov/itl/ai-risk-management-framework

Reynolds, C.W. (1987) 'Flocks, herds and schools: A distributed behavioral model', *ACM SIGGRAPH Computer Graphics*, 21(4), pp. 25-34.

Rolfe, G., Freshwater, D. and Jasper, M. (2001) *Critical reflection in nursing and the helping professions: a user's guide*. Basingstoke: Palgrave Macmillan.

Schön, D.A. (1983) *The reflective practitioner: How professionals think in action*. New York: Basic Books.

Searle, J.R. (1969) *Speech acts: An essay in the philosophy of language*. Cambridge: Cambridge University Press.

Sommer, R. & Paxson, V. (2010) 'Outside the closed world: On using machine learning for network intrusion detection', in *2010 IEEE Symposium on Security and Privacy*. Berkeley: IEEE, pp. 305-316.

Verma, R. & Das, A. (2022) Leveraging Natural Language Processing for Advanced Phishing Detection in Corporate Environments. *IEEE Transactions on Information Forensics and Security*, 17: 1120-1134.

Wang, S., Wan, J., Li, D., and Zhang, C. (2016) 'Towards smart factory for industry 4.0: a self-organized multi-agent system with big data based feedback and coordination', *Computer Networks*, 101, pp. 158–168.

Wooldridge, M. (2009) *An introduction to multiagent systems*. 2nd ed. Chichester: John Wiley & Sons.

World Economic Forum (2022) *How Deep Learning can improve productivity and boost business*. Available at: https://www.weforum.org/agenda/2022/01/deep-learning-business-productivity-revenue/

Yan, B., Zhou, Z., Zhang, L., Zhang, L., Zhou, Z., Miao, D., Li, Z., Li, C. and Zhang, X. (2025) *Beyond self-talk: a communication-centric survey of LLM-based multi-agent systems*. arXiv preprint.

Zimmerman, V. (2019) *Getting to grips with parse trees*. Available at: https://towardsdatascience.com/getting-to-grips-with-parse-trees-6e19e7cd3c3c


