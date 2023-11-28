gpt_response = """Title: "Gold Unveiled: A Precious Metal of Significance"

Subtitle: "Exploring the Value and Impact of Gold in Our World"

Introduction:
Gold, the "king of metals," holds a unique place in human history and the modern world. In this exploration, we uncover the significance of gold, its diverse applications, and its enduring allure.

The Value of Gold:
Gold's intrinsic value extends beyond its aesthetic appeal. It serves as a reliable store of wealth, a symbol of luxury and status, and a vital component in various industries. As a precious metal, gold offers a sense of security and stability in financial markets.

Origins and Mining:
Gold is primarily found in nature in the form of nuggets or as part of mineral ores. Major gold-producing countries, including China, Australia, and South Africa, contribute to the world's gold supply. The process of gold mining involves extracting this precious metal from the Earth's crust.

Market Trends and Investment:
Investing in gold has been a traditional means of diversifying portfolios. Its value often rises during times of economic uncertainty and inflation, making it a valuable hedge. Tracking market trends and understanding the dynamics of gold pricing are crucial for investors.

Deficiency in Gold Investment:
A deficiency in gold investment is akin to missing out on a stabilizing asset in a diversified portfolio. While gold is not essential for daily life, its absence in an investment strategy may expose individuals to risks associated with economic downturns.

The Perils of Gold Overexposure:
Excessive allocation to gold in an investment portfolio can limit diversification and potential returns. Achieving a balanced portfolio is essential to avoid overexposure to any single asset, including gold.

Striking the Right Balance:
Balancing gold intake means judiciously incorporating gold investments within a diversified portfolio. The percentage allocated to gold should align with one's financial goals, risk tolerance, and market conditions. Striking the right balance is key to optimizing the benefits of gold investments.

Monitoring Gold Performance:
Regularly monitoring the performance of gold investments is essential. This involves keeping an eye on market trends, economic indicators, and gold's role within your broader investment strategy. Adjusting your gold holdings as needed ensures your portfolio remains aligned with your financial objectives."""
gpt_response = gpt_response.replace(":\n\n",":\n")
formatted_text = gpt_response.split("\n\n")
breakpoint()
formatted_text1 = ['Title: "The Power of Vitamin E: Unveiling its Health Benefits and Importance"',
                   'Subtitle: "A Comprehensive Guide to Vitamin E: Sources, Functions, Deficiency, and Supplementation"',
                   'Introduction:',
                   'Vitamin E, an essential fat-soluble nutrient, is a powerhouse antioxidant that plays a crucial role in maintaining overall health. In this comprehensive exploration, we will uncover the remarkable benefits of Vitamin E, its food sources, its functions in the body, the consequences of Vitamin E deficiency, and the potential benefits of Vitamin E supplementation.',
                   'The Importance of Vitamin E:',
                   'Vitamin E is a key antioxidant that protects cells from damage caused by free radicals, unstable molecules that can harm DNA, proteins, and lipids. By neutralizing these harmful molecules, Vitamin E helps reduce the risk of chronic diseases such as heart disease and certain types of cancer. Additionally, Vitamin E supports immune function, aids in the formation of red blood cells, and promotes healthy skin and eyes.',
                   'Sources of Vitamin E from Food:',
                   'Various foods provide Vitamin E, with the highest concentrations found in plant-based sources. Nuts and seeds, including almonds, sunflower seeds, and hazelnuts, are rich sources of Vitamin E. Vegetable oils such as sunflower, safflower, and wheat germ oil are also excellent sources. Leafy green vegetables, avocados, and fortified cereals contribute to Vitamin E intake as well.',
                   'Functions of Vitamin E:',
                   "Vitamin E performs several essential functions in the body. As an antioxidant, it protects cell membranes from oxidative damage and reduces inflammation. Vitamin E's ability to maintain healthy immune function allows the body to combat infections and diseases effectively. Additionally, Vitamin E plays a vital role in promoting healthy skin by supporting collagen production and protecting against UV-induced damage.",
                   'Consequences of Vitamin E Deficiency:',
                   'A deficiency in Vitamin E can lead to various health issues. Neurological symptoms such as muscle weakness, poor coordination, and impaired vision may arise. Vitamin E deficiency has also been linked to immune system dysfunction and increased susceptibility to infections. Furthermore, inadequate Vitamin E intake can cause oxidative stress, which may contribute to chronic diseases like heart disease and cognitive decline.',
                   'Benefits of Vitamin E Supplementation:',
                   "While it is ideal to obtain nutrients from food sources, certain individuals may benefit from Vitamin E supplementation. People with malabsorption disorders, such as cystic fibrosis or Crohn's disease, may have difficulty absorbing Vitamin E from their diet. Additionally, individuals with low-fat diets, those who cannot consume nuts or seeds due to allergies, or those with medical conditions that require high doses of Vitamin E may consider supplementation under the guidance of a healthcare professional.",
                   'Risks and Considerations:',
                   'While Vitamin E supplementation can be beneficial in certain situations, it is essential to be cautious about the dosage. High doses of Vitamin E supplements can interfere with blood clotting, increasing the risk of bleeding, especially in individuals taking blood-thinning medications. It is crucial to consult with a healthcare professional before starting any supplementation regimen to determine the appropriate dosage and address potential interactions or contraindications.',
                   'Monitoring Vitamin E Levels:',
                   'Regular monitoring of Vitamin E levels is not typically necessary for individuals with a balanced diet. However, for those with specific health conditions or concerns, healthcare professionals may recommend periodic blood tests to ensure optimal Vitamin E status.',
                   'Conclusion:',
                   'Understanding the importance of Vitamin E, its food sources, functions, and potential health implications is crucial for overall well-being. By incorporating Vitamin E-rich foods into your diet, you can harness the power of antioxidants to protect against chronic diseases and promote optimal health. For those who may require supplementation, proper guidance from healthcare professionals is essential to ensure appropriate dosages and avoid potential interactions. With a balanced approach to Vitamin E intake, you can unlock the full potential of this remarkable nutrient and enhance your quality of life.']

final_dict = {}
try:
    for paragraph in formatted_text:

        lines = paragraph.replace('\n', " ")
        print("lines : ", lines)
        heading, *content = lines.split(': ')

        if len(content) > 1:
            content = " ".join(content)
        else:
            content = content[0]

        final_dict[heading] = content.strip('"')
        print("final_dict : ", final_dict)
except Exception as exp:
    breakpoint()
    print(exp)

if len(final_dict['Title'] + final_dict['Subtitle']) < 100:
    final_title = final_dict.pop('Title', '') + final_dict.pop('Subtitle', '')
else:
    final_title = final_dict['Title'] + final_dict.pop('Subtitle', '')

final_content = ""
for key, val in final_dict.items():
    each_item_content = key + ": " + val
    final_content = final_content + "\n" + each_item_content
print(final_title, "\n", final_content)
breakpoint()

from pictory_selenium import Pictory

pictory_obj = Pictory(final_title, final_content)
pictory_obj.open_pictory_browser()
breakpoint()
pictory_obj.pictory_editor_page()
