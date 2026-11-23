import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_chapter10(doc, helpers):
    add_styled_heading = helpers['add_styled_heading']
    add_body_p = helpers['add_body_p']

    add_styled_heading(doc, "Chapter 10", 1, font_size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=2)
    add_styled_heading(doc, "BIBLIOGRAPHY", 1, font_size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=14)

    references = [
        "1. Breiman, L. (2001). Random Forests. Machine Learning, 45(1), 5–32. DOI: 10.1023/A:1010933404324",
        "2. Chawla, N. V., Bowyer, K. W., Hall, L. O., & Kegelmeyer, W. P. (2002). SMOTE: Synthetic Minority Over-sampling Technique. Journal of Artificial Intelligence Research (JAIR), 16, 321–357. DOI: 10.1613/jair.953",
        "3. Ansari, A. F., Stella, L., et al. (2024). Chronos: Learning the Language of Time Series. Amazon Research & arXiv Preprint. arXiv: 2403.07815",
        "4. Silver, E. A., & Meal, H. C. (1973). A Heuristic for Selecting Lot Size Quantities for the Case of a Deterministic Time-Varying Demand Rate and Discrete Opportunities for Replenishment. Production and Inventory Management, 14(2), 64–74.",
        "5. Fader, P. S., Hardie, B. G. S., & Lee, K. L. (2005). “Counting Your Customers” the Easy Way: An Alternative to the Pareto/NBD Model. Marketing Science, 24(2), 275–284. DOI: 10.1287/mksc.1040.0098",
        "6. Agrawal, R., & Srikant, R. (1994). Fast Algorithms for Mining Association Rules in Large Databases. Proceedings of the 20th International Conference on Very Large Data Bases (VLDB), 487–499.",
        "7. Liu, F. T., Ting, K. M., & Zhou, Z. H. (2008). Isolation Forest. 8th IEEE International Conference on Data Mining (ICDM), 413–422. DOI: 10.1109/ICDM.2008.17",
        "8. Hutto, C. J., & Gilbert, E. (2014). VADER: A Parsimonious Rule-Based Model for Sentiment Analysis of Social Media Text. 8th International AAAI Conference on Weblogs and Social Media (ICWSM), 216–225.",
        "9. Yurdakul, M. (2004). A Decision Support System for Supply Chain Optimization. International Journal of Production Research, 42(17), 3587–3605. DOI: 10.1080/00207540410001696340",
        "10. Chen, D., Sain, S. L., & Guo, K. (2012). Data Mining for the Online Retail Industry: A Case Study of RFM Model-Based Customer Segmentation. International Journal of Electronic Business, 10(3), 215–233. DOI: 10.1504/IJEB.2012.050519",
        "11. Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., et al. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825–2830.",
        "12. McKinney, W. (2010). Data Structures for Statistical Computing in Python. Proceedings of the 9th Python in Science Conference (SciPy 2010), 51–56. DOI: 10.25080/Majora-92bf1928-005",
        "13. Harris, C. R., Millman, K. J., van der Walt, S. J., Gommers, R., Virtanen, P., Cournapeau, D., et al. (2020). Array Programming with NumPy. Nature, 585(7825), 357–362. DOI: 10.1038/s41586-020-2649-2",
        "14. Paszke, A., Gross, S., Massa, F., Lerer, A., Bradbury, J., Chanan, G., et al. (2019). PyTorch: An Imperative Style, High-Performance Deep Learning Library. Advances in Neural Information Processing Systems (NeurIPS), 32, 8024–8035.",
        "15. Box, G. E. P., Jenkins, G. M., Reinsel, G. C., & Ljung, G. M. (2015). Time Series Analysis: Forecasting and Control (5th ed.). John Wiley & Sons, Hoboken, NJ.",
        "16. Hyndman, R. J., & Athanasopoulos, G. (2018). Forecasting: Principles and Practice (2nd ed.). OTexts, Melbourne, Australia.",
        "17. Chopra, S., & Meindl, P. (2016). Supply Chain Management: Strategy, Planning, and Operation (6th ed.). Pearson Education, Boston, MA.",
        "18. Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning: Data Mining, Inference, and Prediction (2nd ed.). Springer-Verlag, New York, NY.",
        "19. Provost, F., & Fawcett, T. (2013). Data Science for Business: What You Need to Know about Data Mining and Data-Analytic Thinking. O'Reilly Media, Sebastopol, CA.",
        "20. Han, J., Kamber, M., & Pei, J. (2011). Data Mining: Concepts and Techniques (3rd ed.). Morgan Kaufmann Publishers, Waltham, MA.",
        "21. Tan, P.-N., Steinbach, M., Karpatne, A., & Kumar, V. (2018). Introduction to Data Mining (2nd ed.). Pearson Education, New York, NY.",
        "22. Streamlit Inc. (2023). Streamlit Documentation: The Fastest Way to Build and Share Data Apps. Retrieved from https://docs.streamlit.io",
        "23. Plotly Technologies Inc. (2023). Plotly Open Source Graphing Library for Python. Retrieved from https://plotly.com/python",
        "24. SQLite Development Team. (2023). SQLite Database Engine Architecture and SQL Reference. Retrieved from https://www.sqlite.org",
        "25. National Institute of Standards and Technology (NIST). (2015). Recommendation for Password-Based Key Derivation: PBKDF2 (Special Publication 800-132). U.S. Department of Commerce."
    ]

    for ref in references:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.first_line_indent = Inches(-0.3)
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(ref)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0, 0, 0)
