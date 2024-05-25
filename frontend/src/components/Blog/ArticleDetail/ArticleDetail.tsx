import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchArticle } from '../../../services'; // Ensure the correct import path
import './ArticleDetail.css'; // Import the CSS file for styling

interface Article {
  id: number;
  slug: string;
  title: string;
  content: string;
  author: string;
  created_at: string;
  updated_at: string;
  image: string;  // Include image field
}

const ArticleDetail: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const [article, setArticle] = useState<Article | null>(null);

  useEffect(() => {
    if (slug) { // Ensure slug is not undefined
      const getArticle = async () => {
        try {
          const article = await fetchArticle(slug);
          setArticle(article);
        } catch (error) {
          console.error('Error fetching the article:', error);
        }
      };

      getArticle();
    }
  }, [slug]);

  if (!article) {
    return <div>Loading...</div>;
  }

  return (
    <div className="article-detail-container">
      <h1 className="article-detail-title">{article.title}</h1>
      {article.image && <img src={article.image} alt={article.title} className="article-detail-image" />}  {/* Display image if available */}
      <div className="article-detail-content" dangerouslySetInnerHTML={{ __html: article.content }} /> {/* Render HTML content */}
      <div className="article-detail-meta">
        <p>Author: {article.author}</p>
        <p>Published on: {new Date(article.created_at).toLocaleDateString()}</p>
      </div>
    </div>
  );
};

export default ArticleDetail;
