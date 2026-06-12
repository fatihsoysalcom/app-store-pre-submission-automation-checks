import re
import urllib.parse

def validate_app_config(config):
    """
    Simulates an automation tool checking common App Store submission requirements.
    This helps prevent rejections due to easily overlooked metadata or configuration issues.
    """
    issues = []

    # 1. Check App Name length (common metadata requirement)
    app_name = config.get("appName")
    if not app_name:
        issues.append("ERROR: 'appName' is missing.")
    elif not (3 <= len(app_name) <= 30):
        issues.append(f"WARNING: 'appName' length ({len(app_name)}) is not between 3 and 30 characters.")
    
    # 2. Check App Version format (e.g., X.Y.Z)
    app_version = config.get("appVersion")
    if not app_version:
        issues.append("ERROR: 'appVersion' is missing.")
    elif not re.match(r"^\d+(\.\d+){0,2}$", app_version):
        issues.append(f"ERROR: 'appVersion' '{app_version}' format is invalid. Expected X.Y.Z.")

    # 3. Check Privacy Policy URL (critical for App Store approval)
    privacy_policy_url = config.get("privacyPolicyURL")
    if not privacy_policy_url:
        issues.append("ERROR: 'privacyPolicyURL' is missing.")
    else:
        # Simple URL format validation
        parsed_url = urllib.parse.urlparse(privacy_policy_url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            issues.append(f"ERROR: 'privacyPolicyURL' '{privacy_policy_url}' is not a valid URL.")
        elif parsed_url.scheme not in ["http", "https"]:
            issues.append(f"WARNING: 'privacyPolicyURL' uses an insecure scheme '{parsed_url.scheme}'. Prefer 'https'.")

    # 4. Check App Description minimum length (for good user experience and discoverability)
    app_description = config.get("appDescription")
    if not app_description:
        issues.append("ERROR: 'appDescription' is missing.")
    elif len(app_description) < 50: # Arbitrary minimum length for a meaningful description
        issues.append(f"WARNING: 'appDescription' is too short ({len(app_description)} chars). Minimum recommended is 50.")

    # 5. Check for required usage descriptions (simulated for common iOS permissions)
    # In a real iOS app, these would be in Info.plist. Here, we simulate checking for their presence.
    required_permissions_for_features = {
        "camera": "NSCameraUsageDescription",
        "photoLibrary": "NSPhotoLibraryUsageDescription"
    }
    declared_permissions_descriptions = config.get("permissions", {})
    
    for feature, required_key in required_permissions_for_features.items():
        if feature in config.get("features", []) and required_key not in declared_permissions_descriptions:
            issues.append(f"ERROR: App declares '{feature}' feature but is missing '{required_key}' usage description.")
        elif required_key in declared_permissions_descriptions and not declared_permissions_descriptions[required_key]:
            issues.append(f"ERROR: '{required_key}' is declared but its description is empty.")
        
    # Simulate a check for a specific feature being enabled but missing a required configuration
    if "inAppPurchases" in config.get("features", []) and not config.get("inAppPurchaseReceiptValidationEndpoint"):
        issues.append("WARNING: In-App Purchases are enabled but 'inAppPurchaseReceiptValidationEndpoint' is missing.")


    if not issues:
        issues.append("SUCCESS: All automated pre-checks passed!")
    return issues

if __name__ == "__main__":
    # Example 1: A configuration with some issues, simulating a potential rejection scenario
    print("--- Running checks for App Config 1 (with issues) ---")
    app_config_1 = {
        "appName": "My App", # Too short
        "appVersion": "1.0",
        "privacyPolicyURL": "ftp://invalid-scheme.com/privacy", # Invalid scheme
        "appDescription": "This is a short description.", # Too short
        "features": ["camera", "inAppPurchases"],
        "permissions": {
            "NSPhotoLibraryUsageDescription": "We need access to your photos."
            # NSCameraUsageDescription is missing, but camera feature is declared
        }
        # inAppPurchaseReceiptValidationEndpoint is missing
    }
    results_1 = validate_app_config(app_config_1)
    for issue in results_1:
        print(f"- {issue}")
    print("\n")

    # Example 2: A configuration that should pass most checks, demonstrating a successful automation run
    print("--- Running checks for App Config 2 (mostly passing) ---")
    app_config_2 = {
        "appName": "My Awesome Productivity App",
        "appVersion": "2.1.3",
        "privacyPolicyURL": "https://www.example.com/privacy-policy",
        "appDescription": "This is a comprehensive description of my awesome productivity app. It helps users manage tasks, track progress, and collaborate with team members efficiently. We prioritize user privacy and data security.",
        "features": ["camera", "photoLibrary", "location", "inAppPurchases"],
        "permissions": {
            "NSCameraUsageDescription": "We need camera access for profile pictures.",
            "NSPhotoLibraryUsageDescription": "We need photo library access to select images.",
            "NSLocationWhenInUseUsageDescription": "We need your location for location-based reminders."
        },
        "inAppPurchaseReceiptValidationEndpoint": "https://api.example.com/validate-receipt"
    }
    results_2 = validate_app_config(app_config_2)
    for issue in results_2:
        print(f"- {issue}")
    print("\n")

    # Example 3: A configuration with a missing critical field, highlighting a severe error
    print("--- Running checks for App Config 3 (missing critical field) ---")
    app_config_3 = {
        "appName": "Test App",
        "appVersion": "1.0.0",
        # privacyPolicyURL is missing
        "appDescription": "A test application for demonstration purposes.",
        "features": []
    }
    results_3 = validate_app_config(app_config_3)
    for issue in results_3:
        print(f"- {issue}")
    print("\n")
