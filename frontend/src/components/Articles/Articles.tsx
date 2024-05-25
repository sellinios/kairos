// src/components/ArticleLatest/ArticleLatest.tsx
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { fetchLatestArticle } from '../../services/apiService'; // Adjust the import path as necessary
import './ArticleLatest.css'; // Import the CSS file for styling

interface Article {
  id: number;
  slug: string;
  title: string;
  content: string;
  author: string;
  image: string;  // Include image field
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
            <Link to={`/articles/${latestArticle.slug}`}>Featured Article: {latestArticle.title}</Link>
          </h2>
          {latestArticle.image && <img src={latestArticle.image} alt={latestArticle.title} />}  {/* Display image if available */}
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
