import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Helmet } from 'react-helmet';
import { useTranslation } from 'react-i18next';
import { fetchArticle } from '../../../services'; // Ensure the correct import path
import './ArticleDetail.css'; // Correct the CSS import path

interface Article {
  id: number;
  slug: string;
  title: string;
  content: string;
  author: string;
  created_at: string;
  updated_at: string;
  image_thumbnail?: string; // Make image fields optional
  image_medium?: string;
  image_large?: string;
}

const ArticleDetail: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const { i18n } = useTranslation(); // Get the current language
  const [article, setArticle] = useState<Article | null>(null);
  const [loading, setLoading] = useState<boolean>(true); // Add loading state
  const [error, setError] = useState<string | null>(null); // Add error state

  useEffect(() => {
    if (slug) { // Ensure slug is not undefined
      const getArticle = async () => {
        try {
          console.log(`Fetching article with slug: ${slug} in language: ${i18n.language}`);
          const article = await fetchArticle(slug, i18n.language); // Use the current language
          console.log('Fetched article:', article);
          setArticle(article);
        } catch (error) {
          console.error('Error fetching the article:', error);
          setError('Error fetching the article.');
        } finally {
          setLoading(false); // Ensure loading is set to false after fetching
        }
      };

      getArticle();
    } else {
      console.error('No slug provided');
      setLoading(false);
      setError('No slug provided.');
    }
  }, [slug, i18n.language]); // Re-fetch article when slug or language changes

  if (loading) {
    return <div>Loading...</div>; // Display loading state
  }

  if (error) {
    return <div>{error}</div>; // Display error message
  }

  if (!article) {
    return <div>Article not found.</div>; // Handle case where article is not found
  }

  return (
    <div className="article-detail-container">
      <Helmet>
        <title>{article.title}</title>
        <meta name="description" content={article.content.substring(0, 150)} />
        <meta name="author" content={article.author} />
      </Helmet>
      <h1 className="article-detail-title">{article.title}</h1>
      {article.image_large && (
        <img
          srcSet={`${article.image_thumbnail} 100w, ${article.image_medium} 300w, ${article.image_large} 600w`}
          sizes="(max-width: 600px) 100vw, (max-width: 900px) 50vw, 33vw"
          src={article.image_large}
          alt={article.title}
          className="article-detail-image"
        />
      )}
      <div className="article-detail-content" dangerouslySetInnerHTML={{ __html: article.content }} /> {/* Render HTML content */}
      <div className="article-detail-meta">
        <p>Author: {article.author}</p>
        <p>Published on: {new Date(article.created_at).toLocaleDateString()}</p>
      </div>
    </div>
  );
};

export default ArticleDetail;
