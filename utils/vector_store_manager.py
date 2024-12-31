from agency_swarm import set_openai_key
import openai
import os
from dotenv import load_dotenv, set_key
from time import sleep
import time

load_dotenv()

# Set OpenAI API key
set_openai_key(os.getenv('OPENAI_API_KEY'))
client = openai.Client()

def get_or_create_vector_store(name="Ecomm Client Policy"):
    """
    Get existing vector store or create a new one if it doesn't exist.
    """
    try:
        # Check if we already have a vector store ID
        existing_vector_store_id = os.getenv('VECTOR_STORE_ID')
        
        if existing_vector_store_id:
            try:
                # Try to retrieve the existing vector store
                vector_store = client.beta.vector_stores.retrieve(existing_vector_store_id)
                print(f"Using existing vector store: {vector_store.id}")
                return vector_store
            except Exception as e:
                print(f"Existing vector store not found: {e}")
                # Continue to create new one if existing one not found
        
        # Create new vector store if none exists
        vector_store = client.beta.vector_stores.create(name=name)
        vector_store_id = vector_store.id
        
        # Save the vector store ID to .env file
        env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        set_key(env_path, 'VECTOR_STORE_ID', vector_store_id)
        
        print(f"Created new vector store '{name}' with ID: {vector_store_id}")
        print(f"Vector store ID has been saved to .env file")
        return vector_store
    except Exception as e:
        print(f"Error with vector store: {e}")
        return None

def upload_files_to_vector_store(vector_store_id, file_paths):
    """
    Upload files to vector store and poll until processing is complete
    """
    SUPPORTED_EXTENSIONS = ['.txt', '.md', '.pdf', '.doc', '.docx', 
                          '.ppt', '.pptx', '.xlsx', '.csv', '.json']
    
    try:
        file_streams = []
        existing_files = list_vector_store_files(vector_store_id)
        
        for path in file_paths:
            if not os.path.exists(path):
                print(f"File not found: {path}")
                continue
                
            _, ext = os.path.splitext(path)
            if ext.lower() not in SUPPORTED_EXTENSIONS:
                print(f"Unsupported file type for {path}. Supported extensions are: {SUPPORTED_EXTENSIONS}")
                continue
                
            print(f"Processing {path}...")
            file_name = os.path.basename(path)
             # Check if the file exists in the vector store
            if any(file_detail.filename == file_name for file_detail in existing_files if hasattr(file_detail,'filename')):
                print(f"File '{file_name}' already exists in vector store. Skipping upload.")
                continue

            # Open and append files to file_streams list
            file_streams.append(open(path, "rb"))
          
        if not file_streams:
            print("No valid files to upload!")
            return None

        print("\nAdding files to vector store...")

        # Upload the file and poll the status
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store_id,
            files=file_streams
        )
            
        print(f"Final status: {file_batch.status}")
        if hasattr(file_batch, 'file_counts'):
           print(f"File counts: {file_batch.file_counts}")

        # Close file streams
        for file in file_streams:
            file.close()
        
        return file_batch
            
    except Exception as e:
        print(f"Error uploading files: {e}")
        # Ensure files are closed even on error
        if 'file_streams' in locals():
          for file in file_streams:
              file.close()
        return None

def list_vector_store_files(vector_store_id):
    """
    List all files currently in the vector store.
    """
    try:
      files = client.beta.vector_stores.files.list(vector_store_id=vector_store_id)
      files_detail = []
      print("\nFiles in vector store:")
      for file in files.data:
        print(f"- File ID: {file.id}")
        # Try to get file details from OpenAI
        try:
            file_details = client.files.retrieve(file.id)
            print(f"  Filename: {file_details.filename}")
            print(f"  Purpose: {file_details.purpose}")
            print(f"  Created at: {file_details.created_at}")
            files_detail.append(file_details)
        except Exception as e:
            print(f"  Unable to retrieve file details: {e}")
      return files_detail
    except Exception as e:
        print(f"Error listing files: {e}")
        return None

if __name__ == "__main__":
    # 1. Get or create vector store
    vector_store = get_or_create_vector_store()
    
    if vector_store:
        # 2. Define paths to your policy files
        policy_files = [
            "docs/faq.txt",
            "docs/plasma.txt" 
        ]
        
        # 3. Upload new files to vector store
        upload_files_to_vector_store(vector_store.id, policy_files)
        
        # 4. List all files in the vector store
        list_vector_store_files(vector_store.id)
