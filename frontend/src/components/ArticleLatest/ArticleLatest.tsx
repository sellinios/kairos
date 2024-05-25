// src/components/ArticleLatest/ArticleLatest.tsx
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { fetchLatestArticle } from '../../services/apiService'; // Adjust the import path as necessary
import './ArticleLatest.css'; // Import the CSS file for styling

interface Article {
  id: number;
  slug: string;  // Add slug field
  title: string;
  content: string;
  author: string;
}

const ArticleLatest: React.FC = () => {
  const [latestArticle, setLatestArticle] = useState<Article | null>(null);

  useEffect(() => {
    const getLatestArticle = async () => {
      try {
        const article = await fetchLatestArticle();
        setLatestArticle(article);
      } catch (error) {
        console.error('Error fetching the latest article:', error);
      }
    };

    getLatestArticle();
  }, []);

  return (
    <div className="article-latest-container">
      {latestArticle ? (
        <div className="article-latest">
          <h2 className="article-latest-title">
            <Link to={`/articles/${latestArticle.slug}`}>Featured Article: {latestArticle.title}</Link>  {/* Use slug */}
          </h2>
          <p className="article-latest-content" dangerouslySetInnerHTML={{ __html: latestArticle.content }} />
          <small className="article-latest-author">By {latestArticle.author}</small>
        </div>
      ) : (
        <div>Loading article...</div>
      )}
    </div>
  );
};

export default ArticleLatest; // Ensure default export
