using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using System.IO;
using System.Net;
using System.Text;
using System.Text.Json;

public class PayrollDetail
{
    public int EmployeeID { get; set; }
    public string EmployeeName { get; set; }
    public decimal Salary { get; set; }
    // Add more properties as per the result set returned by your stored procedure
}

class Program
{
    static string connString = "Data Source=192.168.20.166;Initial Catalog=ATS_HRMS_TEST;User ID=tech;Password=tech;Integrated Security=false;";

    static void Main(string[] args)
    {
        HttpListener listener = new HttpListener();
        listener.Prefixes.Add("http://localhost:5000/");
        listener.Start();
        Console.WriteLine("Listening...");

        while (true)
        {
            HttpListenerContext context = listener.GetContext();
            HttpListenerRequest request = context.Request;
            HttpListenerResponse response = context.Response;

            string responseString = string.Empty;

            switch (request.HttpMethod)
            {
                case "GET":
                    if (request.RawUrl.StartsWith("/payroll/"))
                    {
                        responseString = HandleStoredProcedureRequest(request);
                    }
                    else
                    {
                        responseString = HandleGetRequest(request);
                    }
                    break;
                case "POST":
                    responseString = HandlePostRequest(request);
                    break;
                case "PUT":
                    responseString = HandlePutRequest(request);
                    break;
                case "DELETE":
                    responseString = HandleDeleteRequest(request);
                    break;
                default:
                    response.StatusCode = (int)HttpStatusCode.MethodNotAllowed;
                    break;
            }

            byte[] buffer = Encoding.UTF8.GetBytes(responseString);
            response.ContentLength64 = buffer.Length;
            Stream output = response.OutputStream;
            output.Write(buffer, 0, buffer.Length);
            output.Close();
        }
    }

    static string HandleStoredProcedureRequest(HttpListenerRequest request)
    {
        var segments = request.RawUrl.Split('/');
        if (segments.Length == 3 && int.TryParse(segments[2], out int payrollId))
        {
            List<PayrollDetail> payrollDetails = new List<PayrollDetail>();

            using (SqlConnection conn = new SqlConnection(connString))
            {
                conn.Open();
                using (SqlCommand cmd = new SqlCommand("HR_Monthly_Pay_Sheet_SP", conn))
                {
                    cmd.CommandType = CommandType.StoredProcedure;
                    cmd.Parameters.AddWithValue("@Payroll_ID", payrollId);

                    using (SqlDataReader reader = cmd.ExecuteReader())
                    {
                        while (reader.Read())
                        {
                            PayrollDetail detail = new PayrollDetail
                            {
                                EmployeeID = reader.GetInt32(0),
                                EmployeeName = reader.GetString(1),
                                Salary = reader.GetDecimal(2)
                                // Map other columns as needed
                            };
                            payrollDetails.Add(detail);
                        }
                    }
                }
            }

            return JsonSerializer.Serialize(payrollDetails);
        }
        else
        {
            return "Invalid Payroll ID";
        }
    }

    static string HandleGetRequest(HttpListenerRequest request)
    {
        string responseString = string.Empty;

        using (SqlConnection conn = new SqlConnection(connString))
        {
            conn.Open();

            if (request.RawUrl == "/products")
            {
                string query = "SELECT * FROM Products";
                using (SqlCommand cmd = new SqlCommand(query, conn))
                {
                    using (SqlDataReader reader = cmd.ExecuteReader())
                    {
                        List<Product> products = new List<Product>();
                        while (reader.Read())
                        {
                            products.Add(new Product
                            {
                                Id = reader.GetInt32(0),
                                Name = reader.GetString(1),
                                Price = reader.GetDecimal(2)
                            });
                        }
                        responseString = JsonSerializer.Serialize(products);
                    }
                }
            }
            else if (request.RawUrl.StartsWith("/products/"))
            {
                var segments = request.RawUrl.Split('/');
                if (segments.Length == 3 && int.TryParse(segments[2], out int id))
                {
                    string query = "SELECT * FROM Products WHERE Id = @Id";
                    using (SqlCommand cmd = new SqlCommand(query, conn))
                    {
                        cmd.Parameters.AddWithValue("@Id", id);
                        using (SqlDataReader reader = cmd.ExecuteReader())
                        {
                            if (reader.Read())
                            {
                                Product product = new Product
                                {
                                    Id = reader.GetInt32(0),
                                    Name = reader.GetString(1),
                                    Price = reader.GetDecimal(2)
                                };
                                responseString = JsonSerializer.Serialize(product);
                            }
                            else
                            {
                                responseString = "Product not found";
                            }
                        }
                    }
                }
            }
        }

        return responseString;
    }

    static string HandlePostRequest(HttpListenerRequest request)
    {
        using (StreamReader reader = new StreamReader(request.InputStream, request.ContentEncoding))
        {
            string json = reader.ReadToEnd();
            Product newProduct = JsonSerializer.Deserialize<Product>(json);

            using (SqlConnection conn = new SqlConnection(connString))
            {
                conn.Open();
                string query = "INSERT INTO Products (Name, Price) VALUES (@Name, @Price); SELECT SCOPE_IDENTITY();";
                using (SqlCommand cmd = new SqlCommand(query, conn))
                {
                    cmd.Parameters.AddWithValue("@Name", newProduct.Name);
                    cmd.Parameters.AddWithValue("@Price", newProduct.Price);
                    newProduct.Id = Convert.ToInt32(cmd.ExecuteScalar());
                }
            }

            return $"Product added with ID: {newProduct.Id}";
        }
    }

    static string HandlePutRequest(HttpListenerRequest request)
    {
        var segments = request.RawUrl.Split('/');
        if (segments.Length == 3 && int.TryParse(segments[2], out int id))
        {
            using (StreamReader reader = new StreamReader(request.InputStream, request.ContentEncoding))
            {
                string json = reader.ReadToEnd();
                Product updatedProduct = JsonSerializer.Deserialize<Product>(json);

                using (SqlConnection conn = new SqlConnection(connString))
                {
                    conn.Open();
                    string query = "UPDATE Products SET Name = @Name, Price = @Price WHERE Id = @Id";
                    using (SqlCommand cmd = new SqlCommand(query, conn))
                    {
                        cmd.Parameters.AddWithValue("@Id", id);
                        cmd.Parameters.AddWithValue("@Name", updatedProduct.Name);
                        cmd.Parameters.AddWithValue("@Price", updatedProduct.Price);

                        int rowsAffected = cmd.ExecuteNonQuery();
                        if (rowsAffected > 0)
                        {
                            return $"Product with ID: {id} updated";
                        }
                        else
                        {
                            return "Product not found";
                        }
                    }
                }
            }
        }
        else
        {
            return "Invalid ID";
        }
    }

    static string HandleDeleteRequest(HttpListenerRequest request)
    {
        var segments = request.RawUrl.Split('/');
        if (segments.Length == 3 && int.TryParse(segments[2], out int id))
        {
            using (SqlConnection conn = new SqlConnection(connString))
            {
                conn.Open();
                string query = "DELETE FROM Products WHERE Id = @Id";
                using (SqlCommand cmd = new SqlCommand(query, conn))
                {
                    cmd.Parameters.AddWithValue("@Id", id);

                    int rowsAffected = cmd.ExecuteNonQuery();
                    if (rowsAffected > 0)
                    {
                        return $"Product with ID: {id} deleted";
                    }
                    else
                    {
                        return "Product not found";
                    }
                }
            }
        }
        else
        {
            return "Invalid ID";
        }
    }
}
