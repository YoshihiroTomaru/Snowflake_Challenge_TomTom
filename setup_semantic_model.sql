-- Step 1: Set the context
-- Replace 'YOUR_DATABASE' and 'YOUR_SCHEMA' with your actual database and schema names.
USE DATABASE YOUR_DATABASE;
USE SCHEMA YOUR_SCHEMA;

-- Step 2: Create a stage to upload the YAML file
CREATE OR REPLACE STAGE semantic_model_stage;

-- Step 3: Upload the YAML file to the stage
-- Execute this command from SnowSQL or your local terminal where the YAML file is located.
-- Make sure your connection context (database, schema) is set correctly.
-- PUT file://environmental_model.yml @semantic_model_stage OVERWRITE=TRUE;

-- Step 4: Create the semantic model from the YAML file on the stage
CREATE OR REPLACE SEMANTIC MODEL environmental_analysis_model
  FROM @semantic_model_stage/environmental_model.yml;

-- Step 5: Query using the semantic model
-- You can now query Cortex Analyst by referencing the staged YAML file directly in the API call.
-- Example question: "What is the average temperature by area category last month?"
-- Example question: "Show me the trend of CO2 levels in large size rooms."
