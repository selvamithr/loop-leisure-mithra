/**
 * FAQ Accordion Script
 * Handles expanding and collapsing of FAQ answers.
 */

document.addEventListener('DOMContentLoaded', () => {
    const faqQuestions = document.querySelectorAll('.faq-question');

    faqQuestions.forEach(question => {
        question.addEventListener('click', () => {
            const answer = question.nextElementSibling;
            const icon = question.querySelector('.faq-icon');
            const isExpanded = question.getAttribute('aria-expanded') === 'true';

            // Close all other open answers
            document.querySelectorAll('.faq-question[aria-expanded="true"]').forEach(openQuestion => {
                if (openQuestion !== question) {
                    openQuestion.setAttribute('aria-expanded', 'false');
                    openQuestion.nextElementSibling.style.maxHeight = null;
                    openQuestion.querySelector('.faq-icon').textContent = '+';
                }
            });

            // Toggle current answer
            if (isExpanded) {
                question.setAttribute('aria-expanded', 'false');
                answer.style.maxHeight = null;
                icon.textContent = '+';
            } else {
                question.setAttribute('aria-expanded', 'true');
                answer.style.maxHeight = answer.scrollHeight + 'px';
                icon.textContent = '−';
            }
        });
    });
});
