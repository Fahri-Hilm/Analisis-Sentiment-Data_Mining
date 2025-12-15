// Database configuration
module.exports = {
  development: {
    host: 'localhost',
    port: 5432,
    database: 'sentiment_analysis',
    username: 'admin',
    password: 'dev_password_123'
  },
  production: {
    host: 'postgres',
    port: 5432,
    database: 'sentiment_analysis',
    username: 'admin',
    password: 'prod_password_456'  // Change this for production
  }
};
