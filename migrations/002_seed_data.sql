-- Seed data for testing
-- Based on examples/articles/published_article.json

INSERT INTO news (
    idx,
    news_title,
    news_excerpt,
    newscontent,
    news_content,
    news_image,
    news_image_caption,
    news_url,
    news_author,
    news_date,
    draft,
    featured,
    featured_order
) VALUES (
    0,
    '2024 Sing for Hope Pianos in NYC, New Orleans, Newport News, Paris, & More',
    'Sing for Hope continues to expand the impact and scope of our beloved Pianos program, launching powerful new citywide programs in New York City and cities worldwide.',
    '<p>In 2024, Sing for Hope continues to increase the impact and scope of our beloved Sing for Hope Pianos, launching powerful new citywide programs across all five boroughs of our home base of New York City, as well as the cities of New Orleans, Newport News, Paris, and more.</p>

<p>The Sing for Hope Pianos, one of the world''s largest public art initiatives, places artist-designed pianos in parks and public spaces for anyone and everyone to enjoy. Each Sing for Hope Piano is a unique work of art, created by dedicated artists who believe in the power of "art for all" to foster public health and well-being, equity, and joy. The Sing for Hope Pianos transform everyday spaces into vibrant community hubs, inviting people to come together through music. After their outdoor tenure, the pianos find new homes in schools, hospitals, and community centers, where they continue to inspire and uplift.</p>',
    '{"content": "content"}',
    'https://app.singforhope.org/storage/v1/object/public/uploads/public/news/JJ%20Gonzalez%20Acosta%20-%20Little%20Island%20In%20Manhattan%20SFH%20Bach.jpeg',
    'Sing for Hope Piano ''Bach in NYC'' by JJ Gonzalez Acosta',
    '2024-sing-for-hope-pianos-in-NYC,-new-orleans,-newport-news,-Paris,-and-more',
    NULL,
    '2024-02-22 22:04:28.291+00',
    FALSE,
    FALSE,
    11
);

-- Add a draft article for testing
INSERT INTO news (
    news_title,
    newscontent,
    draft,
    news_author
) VALUES (
    'Spring Fundraiser 2026 - Coming Soon',
    '<p>We''re excited to announce our Spring Fundraiser happening in April 2026!</p>
    
<p>Stay tuned for more details about this exciting event where we''ll be bringing music and art to communities across New York City.</p>',
    TRUE,
    'Newsletter Manager Bot'
);

-- Add another draft for testing bulk operations
INSERT INTO news (
    news_title,
    newscontent,
    draft,
    news_author
) VALUES (
    'Summer Concert Series Announcement',
    '<p>Join us this summer for an incredible concert series in Central Park featuring local and international artists.</p>',
    TRUE,
    'Newsletter Manager Bot'
);
