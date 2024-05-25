import React, { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { fetchLatestArticles } from '../../../services'; // Ensure the correct import path
import './ArticleBlock.css'; // Correct the CSS import path

interface Article {
  id: number;
  slug: string;
  title: string;
  content: string;
  author: string;
  image_thumbnail?: string; // Make image fields optional
  image_medium?: string;
  image_large?: string;
}

const ArticleBlock: React.FC = () => {
  const { i18n } = useTranslation();
  const [latestArticles, setLatestArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null); // Add error state

  useEffect(() => {
    const getLatestArticles = async () => {
      try {
        const articles = await fetchLatestArticles(i18n.language);
        console.log('Fetched articles:', articles); // Log fetched articles
        setLatestArticles(articles);
      } catch (error) {
        console.error('Error fetching the latest articles:', error);
        setError('Error fetching the latest articles.');
      } finally {
        setLoading(false); // Ensure loading is set to false after fetching
      }
    };

    getLatestArticles();
  }, [i18n.language]); // Re-fetch articles when language changes

  if (loading) {
    return <div>Loading articles...</div>;
  }

  if (error) {
    return <div>{error}</div>; // Display error message
  }

  if (latestArticles.length === 0) {
    return <div>No articles found.</div>;
  }

  return (
    <div className="article-block-container">
      <Helmet>
        <title>Latest Articles</title>
        <meta name="description" content="Browse the latest articles on our platform." />
      </Helmet>
      <div className="article-grid">
        {latestArticles.map(article => (
          <div key={article.id} className="article-block">
            <Link to={`/articles/${article.slug}`}>
              {article.image_large && (
                <img
                  srcSet={`${article.image_thumbnail} 100w, ${article.image_medium} 300w, ${article.image_large} 600w`}
                  sizes="(max-width: 600px) 100vw, (max-width: 900px) 50vw, 33vw"
                  src={article.image_large}
                  alt={article.title}
                  className="article-block-image"
                />
              )}
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

export default ArticleBlock;
