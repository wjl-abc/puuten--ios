//
//  WBViewController.m
//  puuten
//
//  Created by wang jialei on 12-8-3.
//
//

#import "WBViewController.h"
#import "ASIFormDataRequest.h"
#import "Constance.h"
@interface WBViewController ()

@end

@implementation WBViewController
@synthesize name;
@synthesize bodyField;
@synthesize bsheader=_bsheader;
@synthesize wb_id=_wb_id;
@synthesize name_string = _name_string;
@synthesize url_string = _url_string;

- (void)setWb_id:(int)wb_id
{
    _wb_id = wb_id;
    
    NSString *wb_url_string = [NSString stringWithFormat:@"/business/wb/%d/", self.wb_id];
    NSURL *nsURL = [[NSURL alloc] initWithString:URL];
    NSURL *wbURL = [NSURL URLWithString:wb_url_string relativeToURL:nsURL];
    ASIFormDataRequest *_request=[ASIFormDataRequest requestWithURL:wbURL];
    __weak ASIFormDataRequest *request = _request;
    [request setPostValue:@"ios" forKey:@"mobile"];
    [request setCompletionBlock:^{
        NSData *responseData = [request responseData];
        NSError* error;
        NSDictionary* json = [NSJSONSerialization JSONObjectWithData:responseData options:kNilOptions error:&error];
        //arrayData = json;
        NSLog(@"%@", [json objectForKey:@"name"]);
        NSLog(@"%@", [json objectForKey:@"body"]);
        //BSHeader *bs = [[BSHeader alloc] init];
        self.name_string = @"mmmm";//[json objectForKey:@"name"];
        self.url_string = @"http://tp2.sinaimg.cn/2105912065/180/5619589260/0";//[json objectForKey:@"avatar_url"];
        //[self.view addSubview:bs ];
        //self.name.text = [json objectForKey:@"name"];
        //self.bodyField.text = [json objectForKey:@"body"];
        //self.bsheader.name = @"mmmm";
        //self.bsheader.avatar_url = @"http://tp2.sinaimg.cn/2105912065/180/5619589260/0";
    }];
    [request setFailedBlock:^{
        
    }];
    
    [request startAsynchronous];
}

- (void)setBsheader:(BSHeader *)bsheader
{
    _bsheader = bsheader;
}

- (void)setName_string:(NSString *)name_string{
    _name_string = name_string;
}

- (void)setUrl_string:(NSString *)url_string{
    _url_string = url_string;
}

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    /*
    NSString *wb_url_string = [NSString stringWithFormat:@"/business/wb/%d/", self.wb_id];
    NSURL *nsURL = [[NSURL alloc] initWithString:URL];
    NSURL *wbURL = [NSURL URLWithString:wb_url_string relativeToURL:nsURL];
    ASIFormDataRequest *_request=[ASIFormDataRequest requestWithURL:wbURL];
    __weak ASIFormDataRequest *request = _request;
    [request setPostValue:@"ios" forKey:@"mobile"];
    [request setCompletionBlock:^{
        NSData *responseData = [request responseData];
        NSError* error;
        NSDictionary* json = [NSJSONSerialization JSONObjectWithData:responseData options:kNilOptions error:&error];
        //arrayData = json;
        NSLog(@"%@", [json objectForKey:@"name"]);
        NSLog(@"%@", [json objectForKey:@"body"]);
        //BSHeader *bs = [[BSHeader alloc] init];
        self.name_string = [json objectForKey:@"name"];
        self.url_string = [json objectForKey:@"avatar_url"];
        //[self.view addSubview:bs ];
        //self.name.text = [json objectForKey:@"name"];
        //self.bodyField.text = [json objectForKey:@"body"];
        //self.bsheader.name = @"mmmm";
        //self.bsheader.avatar_url = @"http://tp2.sinaimg.cn/2105912065/180/5619589260/0";
    }];
    [request setFailedBlock:^{
        
    }];
    
    [request startAsynchronous];
    */ 
    self.bsheader.name = self.name_string;
    self.bsheader.avatar_url = self.url_string;
    //self.bsheader.avatar_url = @"http://tp2.sinaimg.cn/2105912065/180/5619589260/0";
	// Do any additional setup after loading the view.
}

- (void)viewDidAppear:(BOOL)animated
{
    [super viewDidAppear:animated];
    //self.bsheader.name = @"mmmm";
    //self.bsheader.avatar_url = @"http://tp2.sinaimg.cn/2105912065/180/5619589260/0";
}
- (void)viewDidUnload
{
    [self setName:nil];
    [self setBodyField:nil];
    [self setBsheader:nil];
    [super viewDidUnload];
    // Release any retained subviews of the main view.
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

@end
