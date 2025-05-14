function openReportModal(slug) {
                document.getElementById("reportModal-" + slug).style.display = "block";
            }
            
            function closeReportModal(slug) {
                document.getElementById("reportModal-" + slug).style.display = "none";
            }
            
            window.onclick = function(event) {
                document.querySelectorAll(".modal").forEach(modal => {
                    if (event.target === modal) {
                        modal.style.display = "none";
                    }
                });
            }

            function toggleOtherReasonField() {
                var reasonSelect = document.getElementById("reason-select");
                var otherReasonField = document.getElementById("other-reason-field");
        
                if (reasonSelect.value === "Other") {
                    otherReasonField.style.display = "block";
                } else {
                    otherReasonField.style.display = "none";
                }
            }