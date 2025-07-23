"""
Database setup and migration scripts for Confluence Enhancer
"""
import logging
import asyncio
from typing import Optional
import oracledb
from src.utils.config import Settings

logger = logging.getLogger(__name__)

# Database schema SQL scripts
CREATE_TABLES_SQL = """
-- Content table for storing Confluence page data
CREATE TABLE IF NOT EXISTS content (
    id VARCHAR2(100) PRIMARY KEY,
    title VARCHAR2(500) NOT NULL,
    space_key VARCHAR2(50) NOT NULL,
    page_id VARCHAR2(50) NOT NULL,
    url VARCHAR2(1000) NOT NULL,
    content CLOB,
    metadata CLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR2(20) DEFAULT 'active'
);

-- Analysis results table
CREATE TABLE IF NOT EXISTS analysis_results (
    id VARCHAR2(100) PRIMARY KEY,
    content_id VARCHAR2(100) NOT NULL,
    analysis_type VARCHAR2(50) NOT NULL,
    results CLOB,
    confidence_score NUMBER(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (content_id) REFERENCES content(id)
);

-- Visualizations table
CREATE TABLE IF NOT EXISTS visualizations (
    id VARCHAR2(100) PRIMARY KEY,
    content_id VARCHAR2(100) NOT NULL,
    visualization_type VARCHAR2(50) NOT NULL,
    title VARCHAR2(200),
    description VARCHAR2(1000),
    chart_data CLOB,
    chart_config CLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (content_id) REFERENCES content(id)
);

-- Enhancement suggestions table
CREATE TABLE IF NOT EXISTS enhancements (
    id VARCHAR2(100) PRIMARY KEY,
    content_id VARCHAR2(100) NOT NULL,
    suggestion_type VARCHAR2(50) NOT NULL,
    title VARCHAR2(200) NOT NULL,
    description CLOB,
    original_content CLOB,
    enhanced_content CLOB,
    confidence_score NUMBER(3,2),
    status VARCHAR2(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    applied_at TIMESTAMP,
    FOREIGN KEY (content_id) REFERENCES content(id)
);

-- Technology analysis table
CREATE TABLE IF NOT EXISTS technology_analysis (
    id VARCHAR2(100) PRIMARY KEY,
    content_id VARCHAR2(100) NOT NULL,
    technology_name VARCHAR2(100) NOT NULL,
    version_detected VARCHAR2(50),
    category VARCHAR2(50),
    modernization_priority VARCHAR2(20),
    risk_level VARCHAR2(20),
    alternatives CLOB,
    migration_plan CLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (content_id) REFERENCES content(id)
);

-- Reports table
CREATE TABLE IF NOT EXISTS reports (
    id VARCHAR2(100) PRIMARY KEY,
    content_id VARCHAR2(100) NOT NULL,
    report_type VARCHAR2(50) NOT NULL,
    title VARCHAR2(200) NOT NULL,
    summary CLOB,
    detailed_data CLOB,
    export_formats VARCHAR2(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    generated_by VARCHAR2(100),
    FOREIGN KEY (content_id) REFERENCES content(id)
);

-- User sessions table (for authentication)
CREATE TABLE IF NOT EXISTS user_sessions (
    id VARCHAR2(100) PRIMARY KEY,
    user_id VARCHAR2(100) NOT NULL,
    confluence_user VARCHAR2(100),
    access_token CLOB,
    refresh_token CLOB,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Processing queue table (for async tasks)
CREATE TABLE IF NOT EXISTS processing_queue (
    id VARCHAR2(100) PRIMARY KEY,
    task_type VARCHAR2(50) NOT NULL,
    content_id VARCHAR2(100),
    priority NUMBER(1) DEFAULT 1,
    status VARCHAR2(20) DEFAULT 'pending',
    parameters CLOB,
    result CLOB,
    error_message CLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    retry_count NUMBER(2) DEFAULT 0
);
"""

CREATE_INDEXES_SQL = """
-- Performance indexes
CREATE INDEX idx_content_space_key ON content(space_key);
CREATE INDEX idx_content_page_id ON content(page_id);
CREATE INDEX idx_content_status ON content(status);
CREATE INDEX idx_content_updated_at ON content(updated_at);

CREATE INDEX idx_analysis_content_id ON analysis_results(content_id);
CREATE INDEX idx_analysis_type ON analysis_results(analysis_type);
CREATE INDEX idx_analysis_created_at ON analysis_results(created_at);

CREATE INDEX idx_viz_content_id ON visualizations(content_id);
CREATE INDEX idx_viz_type ON visualizations(visualization_type);

CREATE INDEX idx_enhancements_content_id ON enhancements(content_id);
CREATE INDEX idx_enhancements_status ON enhancements(status);
CREATE INDEX idx_enhancements_type ON enhancements(suggestion_type);

CREATE INDEX idx_tech_content_id ON technology_analysis(content_id);
CREATE INDEX idx_tech_name ON technology_analysis(technology_name);
CREATE INDEX idx_tech_priority ON technology_analysis(modernization_priority);

CREATE INDEX idx_reports_content_id ON reports(content_id);
CREATE INDEX idx_reports_type ON reports(report_type);

CREATE INDEX idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_sessions_expires_at ON user_sessions(expires_at);

CREATE INDEX idx_queue_status ON processing_queue(status);
CREATE INDEX idx_queue_priority ON processing_queue(priority);
CREATE INDEX idx_queue_created_at ON processing_queue(created_at);
"""

INSERT_SAMPLE_DATA_SQL = """
-- Sample data for testing
INSERT INTO content (id, title, space_key, page_id, url, content, metadata) VALUES (
    'sample-001',
    'Sample Confluence Page',
    'DEV',
    '123456',
    'https://company.atlassian.net/wiki/spaces/DEV/pages/123456',
    'This is a sample Confluence page with some content for testing.',
    '{"author": "test_user", "last_modified": "2025-01-01", "labels": ["testing", "sample"]}'
);

INSERT INTO analysis_results (id, content_id, analysis_type, results, confidence_score) VALUES (
    'analysis-001',
    'sample-001',
    'content_structure',
    '{"sections": 3, "tables": 1, "images": 2, "links": 5}',
    0.95
);
"""


class DatabaseSetup:
    """Database setup and migration manager"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.connection = None
    
    async def connect(self) -> bool:
        """Connect to Oracle database"""
        try:
            # Initialize Oracle client (thick mode for full functionality)
            oracledb.init_oracle_client()
            
            self.connection = oracledb.connect(
                user=self.settings.ORACLE_USER,
                password=self.settings.ORACLE_PASSWORD,
                dsn=f"{self.settings.ORACLE_HOST}:{self.settings.ORACLE_PORT}/{self.settings.ORACLE_SERVICE}"
            )
            
            logger.info("Successfully connected to Oracle database")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Oracle database: {e}")
            return False
    
    async def create_schema(self) -> bool:
        """Create database schema"""
        try:
            if not self.connection:
                await self.connect()
            
            cursor = self.connection.cursor()
            
            # Execute table creation
            logger.info("Creating database tables...")
            cursor.execute(CREATE_TABLES_SQL)
            
            # Execute index creation
            logger.info("Creating database indexes...")
            cursor.execute(CREATE_INDEXES_SQL)
            
            self.connection.commit()
            cursor.close()
            
            logger.info("Database schema created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create database schema: {e}")
            if self.connection:
                self.connection.rollback()
            return False
    
    async def insert_sample_data(self) -> bool:
        """Insert sample data for testing"""
        try:
            if not self.connection:
                await self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(INSERT_SAMPLE_DATA_SQL)
            self.connection.commit()
            cursor.close()
            
            logger.info("Sample data inserted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to insert sample data: {e}")
            if self.connection:
                self.connection.rollback()
            return False
    
    async def verify_installation(self) -> bool:
        """Verify database installation"""
        try:
            if not self.connection:
                await self.connect()
            
            cursor = self.connection.cursor()
            
            # Check if tables exist
            tables_to_check = [
                'content', 'analysis_results', 'visualizations', 
                'enhancements', 'technology_analysis', 'reports',
                'user_sessions', 'processing_queue'
            ]
            
            for table in tables_to_check:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                logger.info(f"Table {table}: {count} records")
            
            cursor.close()
            logger.info("Database verification completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Database verification failed: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")


async def setup_database():
    """Main database setup function"""
    settings = Settings()
    db_setup = DatabaseSetup(settings)
    
    try:
        # Connect to database
        if not await db_setup.connect():
            logger.error("Failed to connect to database. Please check your configuration.")
            return False
        
        # Create schema
        if not await db_setup.create_schema():
            logger.error("Failed to create database schema.")
            return False
        
        # Insert sample data
        if not await db_setup.insert_sample_data():
            logger.warning("Failed to insert sample data, but schema creation succeeded.")
        
        # Verify installation
        if not await db_setup.verify_installation():
            logger.error("Database verification failed.")
            return False
        
        logger.info("Database setup completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        return False
    
    finally:
        db_setup.close()


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run database setup
    asyncio.run(setup_database())
