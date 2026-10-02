document.addEventListener("DOMContentLoaded", function() {
      const imageInput = document.querySelector('input[type="file"]');
      const previewContainer = document.getElementById('image-preview-container');
      
      let dt = new DataTransfer();

      if (imageInput) {
        imageInput.setAttribute('multiple', 'true');

        imageInput.addEventListener('change', function(event) {
          const files = event.target.files;
          
          for (let i = 0; i < files.length; i++) {
            
            dt.items.add(files[i]);
          }
          
          
          imageInput.files = dt.files;
          renderPreviews();
        });
      }

      function renderPreviews() {
        previewContainer.innerHTML = '';
        
        Array.from(dt.files).forEach((file, index) => {
          if (file.type.startsWith('image/')) {
            const reader = new FileReader();

            reader.onload = function(e) {
              // Wrapper Box
              const wrapper = document.createElement('div');
              wrapper.style.position = 'relative';
              wrapper.style.width = '100px';
              wrapper.style.height = '100px';
              wrapper.style.borderRadius = '8px';
              wrapper.style.overflow = 'hidden';
              wrapper.style.border = '1px solid var(--line, #e2e8f0)';
              wrapper.style.boxShadow = '0 2px 5px rgba(0,0,0,0.05)';
              wrapper.style.background = '#000';

              const img = document.createElement('img');
              img.src = e.target.result;
              img.style.width = '100%';
              img.style.height = '100%';
              img.style.objectFit = 'cover';
              img.style.cursor = 'pointer';
              img.title = "Click to open in new tab";
              
              img.addEventListener('click', function() {
                const newTab = window.open();
                newTab.document.write(`<img src="${e.target.result}" style="width:100%; height:auto; object-fit:contain; background:#111;"/>`);
              });

              const removeBtn = document.createElement('button');
              removeBtn.innerHTML = '&times;';
              removeBtn.type = 'button';
              removeBtn.style.position = 'absolute';
              removeBtn.style.top = '4px';
              removeBtn.style.right = '4px';
              removeBtn.style.background = 'rgba(0, 0, 0, 0.7)';
              removeBtn.style.color = '#fff';
              removeBtn.style.border = 'none';
              removeBtn.style.borderRadius = '50%';
              removeBtn.style.width = '24px';
              removeBtn.style.height = '24px';
              removeBtn.style.font = 'bold 14px/1 sans-serif';
              removeBtn.style.cursor = 'pointer';
              removeBtn.style.display = 'flex';
              removeBtn.style.alignItems = 'center';
              removeBtn.style.justifyContent = 'center';

              removeBtn.addEventListener('click', function(event) {
                event.stopPropagation(); 
                
                const newDt = new DataTransfer();
                const currentFiles = dt.files;
                
                for (let j = 0; j < currentFiles.length; j++) {
                  if (j !== index) {
                    newDt.items.add(currentFiles[j]);
                  }
                }
                
                dt = newDt;
                imageInput.files = dt.files;
                renderPreviews();
              });

              wrapper.appendChild(img);
              wrapper.appendChild(removeBtn);
              previewContainer.appendChild(wrapper);
            }

            reader.readAsDataURL(file);
          }
        });
      }
    });