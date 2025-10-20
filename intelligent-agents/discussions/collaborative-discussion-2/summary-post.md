# Summary Post - Collaborative Discussion 2

## Evolution of Agent Communication: From Formal ACLs to Adaptive Protocols

Our discussion on agent communication languages (ACLs) has provided a clear overview of their foundational role and the evolving landscape of multi-agent coordination. The conversation has effectively contrasted the benefits of formal languages with their inherent limitations, and considered how newer approaches are addressing these challenges.

In my initial post, I focused on how ACLs like KQML enable interoperability in diverse, open systems. Their key advantage, rooted in the speech-act theory of Searle (1969), is that they allow agents to communicate intent through high-level performatives (e.g., 'inform', 'request'), abstracting away from specific implementations (Finin et al., 1994). This facilitates flexible coordination among independently developed agents.

However, as was discussed, the primary drawback of this approach is its reliance on a shared ontology. Without semantic agreement on the terms used in a message, communication can fail. This challenge is significant in open environments where agents may have incomplete or mismatched knowledge, making ontology negotiation a critical but difficult task (Payne and Tamma, 2014).

The feedback from Martyna Antas rightly pointed out that the field is moving beyond these rigid structures. Our course readings support this view, particularly those from Unit 7, which explore how semantic meaning can be acquired automatically from text. Techniques for learning distributed word representations (Mikolov et al., 2013) and identifying semantic relationships (Hearst, 1992) provide a foundation for agents to develop more flexible and emergent communication protocols. These data-driven methods, alongside reinforcement learning and large language models, offer a path to overcoming the bottleneck of pre-defined ontologies by allowing agents to learn and adapt their communication strategies dynamically.

This suggests that while formal ACLs established the core principles of agent communication, the future appears to lie in a spectrum of mechanisms. The insights from natural language processing are enabling a shift towards more adaptive and less brittle forms of communication, potentially combining the explicit intentionality of classic ACLs with the learned flexibility of modern AI.

## References

Finin, T., Weber, J., Wiederhold, G., Genesereth, M., Fritzson, R., McKay, D., McGuire, J., Pelavin, R., Shapiro, S. and Beck, C. (1994) 'KQML as an agent communication language', in *Proceedings of the third international conference on Information and knowledge management*, pp. 456-463.

Hearst, M.A. (1992) 'Automatic acquisition of hyponyms from large text corpora', in *COLING 1992 Volume 2: The 14th International Conference on Computational Linguistics*.

Mikolov, T., Chen, K., Corrado, G. and Dean, J. (2013) 'Efficient estimation of word representations in vector space', *arXiv preprint arXiv:1301.3781*.

Payne, T.R and Tamma, V. (2014) 'Negotiating over ontological correspondences with asymmetric and incomplete knowledge', *Journal of the Brazilian Computer Society*, 20(1), p. 10.

Searle, J.R. (1969) *Speech acts: An essay in the philosophy of language*. Cambridge: Cambridge University Press.

Yan, B., Zhou, Z., Zhang, L., Zhang, L., Zhou, Z., Miao, D., Li, Z., Li, C. and Zhang, X. (2025) *Beyond self-talk: a communication-centric survey of LLM-based multi-agent systems*. arXiv preprint. Available at: https://arxiv.org/abs/2502.14321 (Accessed: 28 September 2025).

Zhu, C., Dastani, M. and Wang, S. (2024) 'A survey of multi-agent deep reinforcement learning with communication', *Autonomous Agents and Multi-Agent Systems*, 38(4), p. 4.

