import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import word_tokenize, pos_tag, sent_tokenize
from nltk.corpus import stopwords
from typing import Dict, List

nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')

class PersonalityAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))

        # 读取CSV文件
        data = pd.read_csv('./vocab_data.csv')

        # 将每一列的数据存储到相应的列表中
        self.emotional_words = data['Emotional Words'].dropna().tolist()
        self.positive_commitment_words = data['Positive Commitment Words'].dropna().tolist()
        self.social_words = data['Social Words'].dropna().tolist()
        self.positive_adjectives = data['Positive Adjectives'].dropna().tolist()
        self.empathetic_words = data['Empathetic Words'].dropna().tolist()
        self.politeness_markers = data['Politeness Markers'].dropna().tolist()
        self.abstract_words = data['Abstract Words'].dropna().tolist()
        self.concrete_words = data['Concrete Words'].dropna().tolist()
        self.modals = data['Modals'].dropna().tolist()
        self.positive_words = data['Positive Words'].dropna().tolist()
        self.negative_words = data['Negative Words'].dropna().tolist()
        self.anxiety_words = data['Anxiety Words'].dropna().tolist()

    def analyze_post(self, post: str) -> Dict[str, float]:
        # 使用 VADER 分析单个 post 的情绪得分
        sentiment_scores = self.analyzer.polarity_scores(post)
        return sentiment_scores

    def get_openness_score(self, posts: List[str]) -> float:
        unique_words = set()
        total_word_count, total_sentences = 0, 0
        abstract_count, concrete_count, total_emotional_words = 0, 0, 0

        for post in posts:
            sentences = sent_tokenize(post)
            total_sentences += len(sentences)

            # 统计所有词汇及独特词汇
            tokens = word_tokenize(post.lower())
            total_word_count += len(tokens)
            unique_words.update(tokens)

            # 计算抽象与具体词汇的数量
            abstract_count += sum(1 for word in tokens if word in self.abstract_words)
            concrete_count += sum(1 for word in tokens if word in self.concrete_words)
            
            # 计算情感词数量
            total_emotional_words += sum(1 for word in tokens if word in self.emotional_words)

        # 词汇多样性，即独特词汇数与总词汇数的比值
        type_token_ratio = len(unique_words) / total_word_count if total_word_count > 0 else 0
        
        # 平均句长，用于反映表达的复杂程度
        avg_sentence_length = total_word_count / total_sentences if total_sentences > 0 else 0
        
        # 抽象词汇与具体词汇的比值
        abstract_concrete_ratio = (abstract_count / concrete_count) if concrete_count > 0 else abstract_count
        
        # 情感词汇的比例
        emotional_word_ratio = total_emotional_words / total_word_count if total_word_count > 0 else 0

        # 综合多个特征计算开放性得分
        openness_score = (
            type_token_ratio * 0.3 +         # 词汇多样性占比30%
            avg_sentence_length * 0.2 +      # 句长占比20%
            abstract_concrete_ratio * 0.3 +  # 抽象-具体词汇比占比30%
            emotional_word_ratio * 0.2       # 情感词占比20%
        ) * 100  
        return openness_score

    def get_conscientiousness_score(self, posts: List[str]) -> float:
        total_word_count = 0
        negative_words_count, commitment_word_count, modal_count = 0, 0, 0

        for post in posts:
            tokens = word_tokenize(post.lower())
            total_word_count += len(tokens)
            # 承诺和时间管理词汇的数量
            commitment_word_count += sum(1 for word in tokens if word in self.positive_commitment_words)
            
            # 模态词数量，用于表示责任感
            modal_count += sum(1 for word in tokens if word in self.modals)
            
            # 使用负面情绪词数量反映拖延或不满情绪
            sentiment_scores = self.analyze_post(post)
            negative_words_count += sentiment_scores["neg"] * len(tokens)*0.001

        # 不同维度计算结果：承诺比例、负面比例、模态比例
        commitment_ratio = commitment_word_count / total_word_count if total_word_count > 0 else 0
        negativity_ratio = negative_words_count / total_word_count if total_word_count > 0 else 0
        modal_ratio = modal_count / total_word_count if total_word_count > 0 else 0

        # 综合各项特征，计算尽责性分数
        conscientiousness_score = (
            commitment_ratio * 0.5 +        # 承诺用词占比50%
            modal_ratio * 0.3 -             # 模态词占比30%
            negativity_ratio * 0.2          # 负面情绪占比20%
        ) * 20000
        return max(0.00, conscientiousness_score)

    def get_extraversion_score(self, posts: List[str]) -> float:
        # print(f"Posts: {posts}")
        total_word_count = 0
        social_word_count, first_person_count, positive_adj_count = 0, 0, 0

        for post in posts:
            tokens = word_tokenize(post)
            total_word_count += len(tokens)
            
            # 社交词汇和第一人称词汇数量
            social_word_count += sum(1 for word, tag in pos_tag(tokens) if word.lower() in self.social_words and tag == 'PRP')
            first_person_count += sum(1 for word, tag in pos_tag(tokens) if word.lower() in ["i", "we"] and tag == 'PRP')
            
            # 积极形容词数量
            positive_adj_count += sum(1 for word in tokens if word.lower() in self.positive_adjectives)

        # 不同维度比例：社交词、第一人称词、积极形容词
        social_word_ratio = social_word_count / total_word_count if total_word_count > 0 else 0
        first_person_ratio = first_person_count / total_word_count if total_word_count > 0 else 0
        positive_adj_ratio = positive_adj_count / total_word_count if total_word_count > 0 else 0

        # 计算外向性分数
        extraversion_score = (
            social_word_ratio * 0.4 +        # 社交词占比40%
            first_person_ratio * 0.3 +       # 第一人称词占比30%
            positive_adj_ratio * 0.3         # 积极形容词占比30%
        ) * 10000  
        return extraversion_score


    def get_agreeableness_score(self, posts: List[str]) -> float:
        total_word_count = 0
        positive_word_count, empathetic_word_count, politeness_count = 0, 0, 0

        for post in posts:
            tokens = word_tokenize(post.lower())
            total_word_count += len(tokens)
            # 计算积极词汇和同理词汇的比例
            positive_word_count += sum(1 for word in tokens if word in self.positive_words)
            empathetic_word_count += sum(1 for word in tokens if word in self.empathetic_words)
            politeness_count += sum(1 for word in tokens if word in self.politeness_markers)

        # 不同维度的比例：积极词、同理词、礼貌标记
        positive_word_ratio = positive_word_count / total_word_count if total_word_count > 0 else 0
        empathetic_word_ratio = empathetic_word_count / total_word_count if total_word_count > 0 else 0
        politeness_ratio = politeness_count / total_word_count if total_word_count > 0 else 0

        # 计算宜人性分数
        agreeableness_score = (
            positive_word_ratio * 0.4 +      # 积极词汇占比40%
            empathetic_word_ratio * 0.3 +    # 同理词汇占比30%
            politeness_ratio * 0.3           # 礼貌标记占比30%
        ) * 20000  
        return agreeableness_score

    def get_neuroticism_score(self, posts: List[str]) -> float:
        sentiment_fluctuation, total_negative_words = 0, 0
        previous_compound_score, total_word_count, anxiety_words_count = None, 0, 0

        for post in posts:
            tokens = word_tokenize(post.lower())
            total_word_count += len(tokens)
            scores = self.analyze_post(post)
            compound_score = scores["compound"]
            total_negative_words += scores["neg"] * len(tokens)
            anxiety_words_count += sum(1 for word in tokens if word in self.anxiety_words)

            # 计算情绪波动，用于反映情绪稳定性
            if previous_compound_score is not None:
                sentiment_fluctuation += abs(compound_score - previous_compound_score)
            previous_compound_score = compound_score

        fluctuation_score = sentiment_fluctuation / len(posts) if len(posts) > 1 else 0
        negative_word_ratio = total_negative_words / total_word_count if total_word_count > 0 else 0
        anxiety_word_ratio = anxiety_words_count / total_word_count if total_word_count > 0 else 0

        # 计算神经质分数
        neuroticism_score = (
            fluctuation_score * 0.4 +        # 情绪波动占比40%
            negative_word_ratio * 0.4 +      # 负面词汇占比40%
            anxiety_word_ratio * 0.2         # 焦虑词汇占比20%
        ) * 1000  
        return neuroticism_score

    def get_personality_traits(self, posts: List[str]) -> Dict[str, float]:
        # 调用五个函数并返回五大性格特质的综合分数
        return {
            "openness": self.get_openness_score(posts),
            "conscientiousness": self.get_conscientiousness_score(posts),
            "extraversion": self.get_extraversion_score(posts),
            "agreeableness": self.get_agreeableness_score(posts),
            "neuroticism": self.get_neuroticism_score(posts)
        }