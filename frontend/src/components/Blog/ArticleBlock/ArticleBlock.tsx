import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { fetchLatestArticles } from '../../../services'; // Ensure the correct import path
import './ArticleBlock.css'; // Import the CSS file for styling

interface Article {
  id: number;
  slug: string;
  title: string;
  content: string;
  author: string;
  image: string; // Include image field
}

const ArticleBlock: React.FC = () => {
  const [latestArticles, setLatestArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const getLatestArticles = async () => {
      try {
        const articles = await fetchLatestArticles();
        console.log('Fetched articles:', articles); // Log fetched articles
        setLatestArticles(articles);
      } catch (error) {
        console.error('Error fetching the latest articles:', error);
      } finally {
        setLoading(false); // Ensure loading is set to false after fetching
      }
    };

    getLatestArticles();
  }, []);

  if (loading) {
    return <div>Loading articles...</div>;
  }

  if (latestArticles.length === 0) {
    return <div>No articles found.</div>;
  }

  return (
    <div className="article-block-container">
      <div className="article-grid">
        {latestArticles.map(article => (
          <div key={article.id} className="article-block">
            <Link to={`/articles/${article.slug}`}>
              <img src={article.image} alt={article.title} className="article-block-image" />
            </Link>
            <h2 className="article-block-title">
              <Link to={`/articles/${article.slug}`}>{article.title}</Link>
            </h2>
            <small className="article-block-author">By {article.author}</small>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ArticleBlock; // Ensure default export
