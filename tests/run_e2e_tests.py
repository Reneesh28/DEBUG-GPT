import requests
import os
import json

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("======================================================================")
    print("RUNNING END-TO-END TESTS FOR DEBUGGPT BACKEND")
    print("======================================================================")
    
    results = {}
    
    # Test 1 - Health Endpoint
    try:
        r = requests.get(f"{BASE_URL}/health")
        results["Test 1: Health Endpoint"] = {
            "status": "PASS" if r.status_code == 200 and r.json().get("status") == "healthy" else "FAIL",
            "code": r.status_code,
            "response": r.json()
        }
    except Exception as e:
        results["Test 1: Health Endpoint"] = {"status": "FAIL", "error": str(e)}

    # Test 2 - Analyze Endpoint (Code)
    cpp_code = """#include <iostream>
using namespace std;
int main()
{
    int arr[5];
    cout << arr[10];
    return 0;
}"""
    try:
        r = requests.post(f"{BASE_URL}/analyze", data={"language": "cpp", "code": cpp_code})
        resp = r.json()
        passed = (
            r.status_code == 200 and
            resp.get("success") is True and
            len(resp.get("issues", [])) > 0 and
            "rag_context" in resp and
            "execution_time" in resp
        )
        results["Test 2: Analyze Endpoint (Code)"] = {
            "status": "PASS" if passed else "FAIL",
            "code": r.status_code,
            "response": resp
        }
    except Exception as e:
        results["Test 2: Analyze Endpoint (Code)"] = {"status": "FAIL", "error": str(e)}

    # Test 3 - Analyze Endpoint (Upload)
    try:
        # Write temporary main.cpp
        with open("temp_main.cpp", "w", encoding="utf-8") as f:
            f.write(cpp_code)
            
        with open("temp_main.cpp", "rb") as f:
            files = {"file": ("main.cpp", f, "text/plain")}
            r = requests.post(f"{BASE_URL}/analyze", data={"language": "cpp"}, files=files)
            
        os.remove("temp_main.cpp")
        resp = r.json()
        passed = (
            r.status_code == 200 and
            resp.get("success") is True and
            len(resp.get("issues", [])) > 0 and
            "rag_context" in resp and
            "execution_time" in resp
        )
        results["Test 3: Analyze Endpoint (Upload)"] = {
            "status": "PASS" if passed else "FAIL",
            "code": r.status_code,
            "response": resp
        }
    except Exception as e:
        results["Test 3: Analyze Endpoint (Upload)"] = {"status": "FAIL", "error": str(e)}

    # Test 4 - Debug Endpoint
    py_debug_code = "for i in range(10):\n    print(x)"
    try:
        r = requests.post(f"{BASE_URL}/debug", data={"language": "python", "code": py_debug_code})
        resp = r.json()
        has_undefined_var = any("Undefined variable" in issue.get("message", "") or "Undefined variable" in issue.get("issue", "") for issue in resp.get("issues", []))
        passed = (
            r.status_code == 200 and
            resp.get("success") is True and
            has_undefined_var and
            len(resp.get("debug_suggestions", [])) > 0
        )
        results["Test 4: Debug Endpoint"] = {
            "status": "PASS" if passed else "FAIL",
            "code": r.status_code,
            "response": resp
        }
    except Exception as e:
        results["Test 4: Debug Endpoint"] = {"status": "FAIL", "error": str(e)}

    # Test 5 - Explain Endpoint
    try:
        r = requests.post(f"{BASE_URL}/explain", json={"error": "Segmentation Fault", "language": "cpp"})
        resp = r.json()
        passed = (
            r.status_code == 200 and
            resp.get("success") is True and
            "technical" in resp and
            "beginner" in resp and
            "analogy" in resp and
            "references" in resp
        )
        results["Test 5: Explain Endpoint"] = {
            "status": "PASS" if passed else "FAIL",
            "code": r.status_code,
            "response": resp
        }
    except Exception as e:
        results["Test 5: Explain Endpoint"] = {"status": "FAIL", "error": str(e)}

    # Test 6 - Optimize Endpoint
    cpp_opt_code = """for(int i=0;i<n;i++)
{
    for(int j=0;j<n;j++)
    {
    }
}"""
    try:
        r = requests.post(f"{BASE_URL}/optimize", data={"language": "cpp", "code": cpp_opt_code})
        resp = r.json()
        passed = (
            r.status_code == 200 and
            resp.get("success") is True and
            "recommendations" in resp and
            "rag_context" in resp
        )
        results["Test 6: Optimize Endpoint"] = {
            "status": "PASS" if passed else "FAIL",
            "code": r.status_code,
            "response": resp
        }
    except Exception as e:
        results["Test 6: Optimize Endpoint"] = {"status": "FAIL", "error": str(e)}

    # Test 7 - Invalid Language (java)
    try:
        r = requests.post(f"{BASE_URL}/analyze", data={"language": "java", "code": "system.out.println();"})
        resp = r.json()
        results["Test 7: Invalid Language"] = {
            "status": "PASS" if r.status_code == 422 else "FAIL",
            "code": r.status_code,
            "response": resp
        }
    except Exception as e:
        results["Test 7: Invalid Language"] = {"status": "FAIL", "error": str(e)}

    # Test 8 - Empty Code
    try:
        r = requests.post(f"{BASE_URL}/analyze", data={"language": "cpp", "code": ""})
        resp = r.json()
        # Should raise 400 bad request (since FastAPI Form field gets empty string, which results in "not code" being True)
        # or 422 since Pydantic does min_length=1 validation. Let's see what it returns.
        results["Test 8: Empty Code"] = {
            "status": "PASS" if r.status_code in (400, 422) else "FAIL",
            "code": r.status_code,
            "response": resp
        }
    except Exception as e:
        results["Test 8: Empty Code"] = {"status": "FAIL", "error": str(e)}

    # Test 9 - Unsupported File (.pdf)
    try:
        with open("temp_example.pdf", "w") as f:
            f.write("dummy pdf content")
            
        with open("temp_example.pdf", "rb") as f:
            files = {"file": ("example.pdf", f, "application/pdf")}
            r = requests.post(f"{BASE_URL}/analyze", data={"language": "cpp"}, files=files)
            
        os.remove("temp_example.pdf")
        resp = r.json()
        results["Test 9: Unsupported File"] = {
            "status": "PASS" if r.status_code == 415 else "FAIL",
            "code": r.status_code,
            "response": resp
        }
    except Exception as e:
        results["Test 9: Unsupported File"] = {"status": "FAIL", "error": str(e)}

    # Test 10 - Empty File
    try:
        with open("temp_empty.cpp", "w") as f:
            pass
            
        with open("temp_empty.cpp", "rb") as f:
            files = {"file": ("empty.cpp", f, "text/plain")}
            r = requests.post(f"{BASE_URL}/analyze", data={"language": "cpp"}, files=files)
            
        os.remove("temp_empty.cpp")
        resp = r.json()
        results["Test 10: Empty File"] = {
            "status": "PASS" if r.status_code == 400 else "FAIL",
            "code": r.status_code,
            "response": resp
        }
    except Exception as e:
        results["Test 10: Empty File"] = {"status": "FAIL", "error": str(e)}

    # Test 11 - Large File
    try:
        with open("temp_large.cpp", "wb") as f:
            # write 6MB of spaces
            f.write(b" " * (6 * 1024 * 1024 + 10))
            
        with open("temp_large.cpp", "rb") as f:
            files = {"file": ("large.cpp", f, "text/plain")}
            r = requests.post(f"{BASE_URL}/analyze", data={"language": "cpp"}, files=files)
            
        os.remove("temp_large.cpp")
        resp = r.json()
        results["Test 11: Large File"] = {
            "status": "PASS" if r.status_code == 413 else "FAIL",
            "code": r.status_code,
            "response": resp
        }
    except Exception as e:
        results["Test 11: Large File"] = {"status": "FAIL", "error": str(e)}

    # Test 12 - UTF-8 Validation
    try:
        with open("temp_binary.cpp", "wb") as f:
            # invalid UTF-8 bytes
            f.write(b"\xff\xfe\xfd\xfc")
            
        with open("temp_binary.cpp", "rb") as f:
            files = {"file": ("binary.cpp", f, "application/octet-stream")}
            r = requests.post(f"{BASE_URL}/analyze", data={"language": "cpp"}, files=files)
            
        os.remove("temp_binary.cpp")
        resp = r.json()
        results["Test 12: UTF-8 Validation"] = {
            "status": "PASS" if r.status_code == 400 and "UTF-8" in resp.get("details", "") else "FAIL",
            "code": r.status_code,
            "response": resp
        }
    except Exception as e:
        results["Test 12: UTF-8 Validation"] = {"status": "FAIL", "error": str(e)}

    # Test 13 - Swagger Docs
    try:
        r_docs = requests.get(f"{BASE_URL}/docs")
        r_openapi = requests.get(f"{BASE_URL}/openapi.json")
        openapi = r_openapi.json()
        paths = openapi.get("paths", {})
        schemas = openapi.get("components", {}).get("schemas", {})
        
        has_endpoints = (
            "/health" in paths and
            "/analyze" in paths and
            "/debug" in paths and
            "/explain" in paths and
            "/optimize" in paths
        )
        has_schemas = (
            "AnalyzeResponse" in schemas and
            "DebugResponse" in schemas and
            "ExplainResponse" in schemas and
            "OptimizeResponse" in schemas and
            "HealthResponse" in schemas
        )
        passed = r_docs.status_code == 200 and r_openapi.status_code == 200 and has_endpoints and has_schemas
        results["Test 13: Swagger Docs"] = {
            "status": "PASS" if passed else "FAIL",
            "code": r_openapi.status_code,
            "has_endpoints": has_endpoints,
            "has_schemas": has_schemas
        }
    except Exception as e:
        results["Test 13: Swagger Docs"] = {"status": "FAIL", "error": str(e)}

    # Test 15 - Rule Engine Verification (Known samples)
    try:
        # Off-by-one
        r_obo = requests.post(f"{BASE_URL}/analyze", data={"language": "cpp", "code": "for(int i = 0; i <= n; i++) {}"})
        obo_passed = any(issue["issue"] == "Possible off-by-one error" for issue in r_obo.json().get("issues", []))
        
        # Division by zero
        r_dbz = requests.post(f"{BASE_URL}/analyze", data={"language": "python", "code": "x = 5 / 0"})
        dbz_passed = any("division by zero" in issue["message"].lower() or "division by zero" in issue["issue"].lower() for issue in r_dbz.json().get("issues", []))
        
        # Missing import / module
        r_mi = requests.post(f"{BASE_URL}/analyze", data={"language": "python", "code": "import non_existent_module_foo"})
        mi_passed = any("Missing module" in issue["issue"] for issue in r_mi.json().get("issues", []))

        # Infinite loop
        r_il = requests.post(f"{BASE_URL}/analyze", data={"language": "cpp", "code": "while(true) {}"})
        il_passed = any("Possible infinite loop" in issue["issue"] for issue in r_il.json().get("issues", []))

        # Null pointer
        # C++ Null pointer pattern: e.g. dereferencing nullptr
        # Let's check cpp_rules.py or logical_rules.py to see how null pointer is detected.
        # Actually, let's look for null pointer rules in those files if needed.
        # But we can verify obo, dbz, mi, il first.
        passed = obo_passed and dbz_passed and mi_passed and il_passed
        results["Test 15: Rule Engine"] = {
            "status": "PASS" if passed else "FAIL",
            "obo_passed": obo_passed,
            "dbz_passed": dbz_passed,
            "mi_passed": mi_passed,
            "il_passed": il_passed,
            "responses": {
                "obo": r_obo.json().get("issues"),
                "dbz": r_dbz.json().get("issues"),
                "mi": r_mi.json().get("issues"),
                "il": r_il.json().get("issues")
            }
        }
    except Exception as e:
        results["Test 15: Rule Engine"] = {"status": "FAIL", "error": str(e)}

    # Test 16 - RAG verification
    try:
        r = requests.post(f"{BASE_URL}/analyze", data={"language": "cpp", "code": cpp_code})
        resp = r.json()
        rag_context = resp.get("rag_context", [])
        
        # Check Top 5
        len_ok = len(rag_context) == 5
        
        # Check Distance sorted (ascending)
        distances = [item["distance"] for item in rag_context]
        sorted_ok = distances == sorted(distances)
        
        # Check properties
        props_ok = all(
            "id" in item and 
            "document" in item and 
            "metadata" in item and 
            "distance" in item and 
            "collection" in item 
            for item in rag_context
        )
        
        passed = len_ok and sorted_ok and props_ok
        results["Test 16: RAG Verification"] = {
            "status": "PASS" if passed else "FAIL",
            "len_ok": len_ok,
            "sorted_ok": sorted_ok,
            "props_ok": props_ok,
            "distances": distances
        }
    except Exception as e:
        results["Test 16: RAG Verification"] = {"status": "FAIL", "error": str(e)}

    # Test 17 - Error Handling (Force Exception)
    try:
        r = requests.get(f"{BASE_URL}/test-error")
        resp = r.json()
        passed = (
            r.status_code == 500 and
            resp.get("success") is False and
            resp.get("error") == "Internal Server Error" and
            resp.get("details") == "An unexpected error occurred while processing the request."
        )
        results["Test 17: Error Handling"] = {
            "status": "PASS" if passed else "FAIL",
            "code": r.status_code,
            "response": resp
        }
    except Exception as e:
        results["Test 17: Error Handling"] = {"status": "FAIL", "error": str(e)}

    # Test 18 - Response Validation (Pydantic schemas match)
    # We can verify that responses from successful endpoints map properly to response fields without unexpected None/errors.
    # We'll check AnalyzeResponse, DebugResponse, ExplainResponse, OptimizeResponse, HealthResponse.
    try:
        health_ok = "status" in results["Test 1: Health Endpoint"]["response"] and "version" in results["Test 1: Health Endpoint"]["response"]
        analyze_ok = all(k in results["Test 2: Analyze Endpoint (Code)"]["response"] for k in ["success", "language", "issues", "rag_context", "execution_time"])
        debug_ok = all(k in results["Test 4: Debug Endpoint"]["response"] for k in ["success", "issues", "debug_suggestions", "rag_context", "execution_time"])
        explain_ok = all(k in results["Test 5: Explain Endpoint"]["response"] for k in ["success", "technical", "beginner", "analogy", "references", "execution_time"])
        optimize_ok = all(k in results["Test 6: Optimize Endpoint"]["response"] for k in ["success", "current_complexity", "optimized_complexity", "recommendations", "rag_context", "execution_time"])
        
        passed = health_ok and analyze_ok and debug_ok and explain_ok and optimize_ok
        results["Test 18: Response Validation"] = {
            "status": "PASS" if passed else "FAIL",
            "health_ok": health_ok,
            "analyze_ok": analyze_ok,
            "debug_ok": debug_ok,
            "explain_ok": explain_ok,
            "optimize_ok": optimize_ok
        }
    except Exception as e:
        results["Test 18: Response Validation"] = {"status": "FAIL", "error": str(e)}

    print("\nE2E Test Summary:")
    print("----------------------------------------------------------------------")
    for test_name, test_info in results.items():
        print(f"{test_name:40} : {test_info['status']}")
    print("======================================================================\n")
    
    # Save test results JSON
    with open("e2e_results.json", "w") as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    run_tests()
